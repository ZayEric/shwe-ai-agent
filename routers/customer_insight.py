from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.customer_insight_service import (
    analyze_customer_insight,
    get_executive_summary,
    ask_business_question,
    get_recommendations,
    get_customer_segments
)

router = APIRouter(
    prefix="/customer-insight",
    tags=["Customer Intelligence"]
)


class QuestionRequest(BaseModel):
    question: str


@router.post("/analyze")
def analyze():

    """
    Read all SharePoint documents,
    analyze using Azure OpenAI,
    generate insight.json
    """

    try:

        result = analyze_customer_insight()

        return {
            "success": True,
            "message": "Customer insight generated successfully.",
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/summary")
def summary():

    """
    Executive summary
    """

    try:

        summary = get_executive_summary()

        return {
            "success": True,
            "summary": summary
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/questions")
def ask(request: QuestionRequest):

    """
    Executive Q&A
    """

    try:

        answer = ask_business_question(request.question)

        return {
            "success": True,
            "question": request.question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/recommendation")
def recommendation():

    """
    AI Product Recommendation
    """

    try:

        result = get_recommendations()

        return {
            "success": True,
            "recommendation": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/segments")
def segments():

    """
    Customer Segmentation
    """

    try:

        segments = get_customer_segments()

        return {
            "success": True,
            "segments": segments
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
