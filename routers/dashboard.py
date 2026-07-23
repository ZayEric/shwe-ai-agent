from fastapi import APIRouter

from services.customer_insight_service import (
    get_dashboard
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard():

    return get_dashboard()


@router.get("/kpis")
def kpis():

    return get_dashboard().get(
        "kpis",
        {}
    )


@router.get("/competitors")
def competitors():

    return get_dashboard().get(
        "competitor_scores",
        []
    )


@router.get("/wallet")
def wallet():

    return get_dashboard().get(
        "wallet_benchmark",
        []
    )


@router.get("/ibmb")
def ibmb():

    return get_dashboard().get(
        "ibmb_benchmark",
        []
    )


@router.get("/campaign")
def campaign():

    return get_dashboard().get(
        "campaign_summary",
        []
    )


@router.get("/feature-gap")
def feature_gap():

    return get_dashboard().get(
        "feature_gap",
        []
    )


@router.get("/customer-voice")
def customer_voice():

    return get_dashboard().get(
        "customer_voice",
        []
    )


@router.get("/swot")
def swot():

    return get_dashboard().get(
        "swot",
        {}
    )


@router.get("/recommendations")
def recommendations():

    return get_dashboard().get(
        "recommendations",
        []
    )
