from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.scene import Scene, SceneStatus
from app.schemas.scene import SceneCreate, SceneResponse, SceneDetail, SceneUpdate
from app.core.security import get_current_user
from app.services.animation import generate_animation
from uuid import UUID

router = APIRouter()

@router.post("/{project_id}/scenes", response_model=SceneResponse)
def create_scene(
    project_id: UUID,
    scene: SceneCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if project exists and belongs to the user
    project = db.query(Project).filter(
        Project.id == project_id, 
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create scene
    db_scene = Scene(
        project_id=project_id,
        prompt=scene.prompt,
        order=scene.order,
        status=SceneStatus.PENDING
    )
    db.add(db_scene)
    db.commit()
    db.refresh(db_scene)
    
    # Generate animation in the background
    background_tasks.add_task(generate_animation, db_scene.id)
    
    return db_scene

@router.get("/{project_id}/scenes", response_model=List[SceneResponse])
def get_scenes(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if project exists and belongs to the user
    project = db.query(Project).filter(
        Project.id == project_id, 
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    scenes = db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.order).all()
    return scenes

@router.get("/{project_id}/scenes/{scene_id}", response_model=SceneDetail)
def get_scene(
    project_id: UUID,
    scene_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Check if project exists and belongs to the user
        project = db.query(Project).filter(
            Project.id == project_id, 
            Project.user_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        scene = db.query(Scene).filter(
            Scene.id == scene_id,
            Scene.project_id == project_id
        ).first()
        if not scene:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scene not found"
            )
        return scene
    except ValueError:
        # Handle invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

@router.put("/{project_id}/scenes/{scene_id}", response_model=SceneResponse)
def update_scene(
    project_id: UUID,
    scene_id: UUID,
    scene_update: SceneUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Check if project exists and belongs to the user
        project = db.query(Project).filter(
            Project.id == project_id, 
            Project.user_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        db_scene = db.query(Scene).filter(
            Scene.id == scene_id,
            Scene.project_id == project_id
        ).first()
        if not db_scene:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scene not found"
            )
        
        # Update scene fields
        update_data = scene_update.model_dump(exclude_unset=True)
        
        # Check if we need to regenerate animation
        regenerate = False
        
        # Regenerate if prompt is updated
        if "prompt" in update_data and update_data["prompt"] != db_scene.prompt:
            regenerate = True
            
        # Regenerate if status is changed from FAILED to PENDING
        if ("status" in update_data and 
            update_data["status"] == SceneStatus.PENDING and 
            db_scene.status == SceneStatus.FAILED):
            regenerate = True
        
        # Apply updates
        for field, value in update_data.items():
            setattr(db_scene, field, value)
        
        if regenerate:
            db_scene.status = SceneStatus.PENDING
            background_tasks.add_task(generate_animation, db_scene.id)
        
        db.commit()
        db.refresh(db_scene)
        return db_scene
    except ValueError:
        # Handle invalid UUID format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

@router.delete("/{project_id}/scenes/{scene_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scene(
    project_id: UUID,
    scene_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if project exists and belongs to the user
    project = db.query(Project).filter(
        Project.id == project_id, 
        Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_scene = db.query(Scene).filter(
        Scene.id == scene_id,
        Scene.project_id == project_id
    ).first()
    if not db_scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene not found"
        )
    
    db.delete(db_scene)
    db.commit()
    return None 