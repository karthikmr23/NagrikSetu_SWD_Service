with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\applications.py", "r", encoding="utf-8") as f:
    text = f.read()

old_code = '''@router.post("/schemes/{scheme_id}/applications", response_model=ApplicationResponse)
def submit_scheme_application(
    scheme_id: int,
    app_in: ApplicationSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Verify citizen ID ownership
    verify_citizen_ownership(app_in.citizen_id, current_user)'''

new_code = '''@router.post("/schemes/{scheme_id}/applications", response_model=ApplicationResponse)
def submit_scheme_application(
    scheme_id: int,
    app_in: ApplicationSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Enforce role restriction: Only CITIZEN users can apply for welfare schemes
    user_role = (current_user.get("role") or "").upper()
    if user_role != "CITIZEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Administrative accounts (Welfare Officers and Platform Admins) cannot submit citizen welfare scheme applications."
        )

    # Verify citizen ID ownership
    verify_citizen_ownership(app_in.citizen_id, current_user)'''

if old_code in text:
    text = text.replace(old_code, new_code)
    with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\applications.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated submit_scheme_application in applications.py")
else:
    print("Could not find old_code in applications.py")
