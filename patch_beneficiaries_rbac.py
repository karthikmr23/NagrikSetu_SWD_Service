with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\beneficiaries.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace list_beneficiaries signature and implementation
old_list = '''@router.get("/beneficiaries", response_model=List[BeneficiaryResponse])
def list_beneficiaries(
    scheme_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Beneficiary)
    if scheme_id:
        query = query.filter(Beneficiary.scheme_id == scheme_id)
    if status_filter:
        query = query.filter(Beneficiary.status == status_filter.upper())
    return query.order_by(Beneficiary.id.desc()).offset(skip).limit(limit).all()

@router.get("/beneficiaries/{beneficiary_id}", response_model=BeneficiaryResponse)
def get_beneficiary_details(beneficiary_id: int, db: Session = Depends(get_db)):
    ben = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary record not found")
    return ben'''

new_list = '''@router.get("/beneficiaries", response_model=List[BeneficiaryResponse])
def list_beneficiaries(
    scheme_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}

    query = db.query(Beneficiary)
    if role not in admin_roles:
        # Citizen role: strictly restrict to their own citizen_id
        citizen_id = current_user.get("citizen_id") or current_user.get("sub")
        query = query.filter(Beneficiary.citizen_id == citizen_id)
    
    if scheme_id:
        query = query.filter(Beneficiary.scheme_id == scheme_id)
    if status_filter:
        query = query.filter(Beneficiary.status == status_filter.upper())
    return query.order_by(Beneficiary.id.desc()).offset(skip).limit(limit).all()

@router.get("/beneficiaries/{beneficiary_id}", response_model=BeneficiaryResponse)
def get_beneficiary_details(
    beneficiary_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ben = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
    if not ben:
        raise HTTPException(status_code=404, detail="Beneficiary record not found")

    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}
    if role not in admin_roles:
        citizen_id = current_user.get("citizen_id") or current_user.get("sub")
        if ben.citizen_id != citizen_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You are not authorized to view another citizen's beneficiary record."
            )
    return ben'''

old_dbt_tx = '''@router.get("/dbt/transactions", response_model=List[DbtTransactionResponse])
def list_dbt_transactions(
    beneficiary_id: Optional[int] = None,
    scheme_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):'''

new_dbt_tx = '''@router.get("/dbt/transactions", response_model=List[DbtTransactionResponse])
def list_dbt_transactions(
    beneficiary_id: Optional[int] = None,
    scheme_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    role = (current_user.get("role") or "CITIZEN").upper()
    admin_roles = {"ADMINISTRATOR", "WELFARE_OFFICER", "GOVERNMENT_WELFARE_ADMIN", "SWD_ADMIN", "PLATFORM_ADMIN"}'''

if old_list in text:
    text = text.replace(old_list, new_list)
    print("Replaced list_beneficiaries and get_beneficiary_details")
else:
    print("Could not find old_list")

if old_dbt_tx in text:
    text = text.replace(old_dbt_tx, new_dbt_tx)
    print("Replaced list_dbt_transactions")
else:
    print("Could not find old_dbt_tx")

# Also in list_dbt_transactions, if role is citizen, filter by beneficiary's citizen_id
old_query_dbt = '''    query = db.query(DbtTransaction)
    if beneficiary_id:'''

new_query_dbt = '''    query = db.query(DbtTransaction)
    if role not in admin_roles:
        citizen_id = current_user.get("citizen_id") or current_user.get("sub")
        query = query.join(Beneficiary, DbtTransaction.beneficiary_id == Beneficiary.id).filter(Beneficiary.citizen_id == citizen_id)
    if beneficiary_id:'''

if old_query_dbt in text:
    text = text.replace(old_query_dbt, new_query_dbt)
    print("Replaced query_dbt")
else:
    print("Could not find old_query_dbt")

with open(r"C:\Users\karth\OneDrive\Documents\NagrikSetu_SWD_Final\backend\app\routers\beneficiaries.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated beneficiaries.py successfully")
