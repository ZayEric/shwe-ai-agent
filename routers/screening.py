from fastapi import APIRouter

from services.screening_service import run_screening

router = APIRouter()


@router.post("/screening")
def screening():

    return run_screening()
