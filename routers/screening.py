@router.post("/screen")
def screen_customer(data: dict):

    return screening_service.screen_customer(data)
