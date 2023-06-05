from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import get_current_competence
from backend.api.dependencies import ListPageParams
from backend.database import get_db
from backend.api.queries import competencies as queries
from backend.api.schemas import competencies as schemas
from backend.models.competencies import Competence
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/competencies')


@router.get('/', response_model=LimitOffsetPage[schemas.Competence])
def get_competencies(params: ListPageParams = Depends(),
                     db: Session = Depends(get_db)):
    return queries.get_competencies(db, params)


@router.get('/{competence_id}', response_model=schemas.OneCompetence)
def get_competence(competence: Competence = Depends(get_current_competence)):
    return competence


@router.post('/', response_model=schemas.OneCompetence, dependencies=[Depends(admin_only)])
def create_competence(competence: schemas.CreateCompetence,
                      db: Session = Depends(get_db)):
    return queries.create_competence(db, competence)


@router.delete('/{competence_id}', status_code=204, dependencies=[Depends(admin_only)])
def delete_competence(competence: Competence = Depends(get_current_competence),
                       db: Session = Depends(get_db)):
    queries.delete_competence(db, competence)
    return {}


@router.patch('/{competence_id}', response_model=schemas.OneCompetence)
def patch_competence(competence: schemas.PatchCompetence,
                     competence_to_patch: Competence = Depends(get_current_competence),
                     db: Session = Depends(get_db)):
    queries.patch_competence(db, competence_to_patch, competence)
    return competence_to_patch
