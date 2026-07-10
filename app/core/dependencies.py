from fastapi import Depends, HTTPException, status
from app.security.auth import get_current_user
from app.models.user import User

def verify_admin_token(current_user: User = Depends(get_current_user)):
    # تحقق أولاً من وجود خاصية is_admin أو أدرجها بحذر لتجنب AttributeError
    is_admin = getattr(current_user, 'is_admin', False)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول: يتطلب صلاحيات مدير"
        )
    return current_user

def require_seller(current_user: User = Depends(get_current_user)):
    """
    التحقق من هوية المستخدم وتمرير بياناته كـ dict متوافق 
    مع متطلبات الأجزاء البرمجية المعتمدة عليه.
    """
    if not current_user or not getattr(current_user, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="جلسة العمل غير صالحة أو الحساب غير نشط"
        )
    
    # تحويل الكائن برمجياً إلى قاموس لتلبية نداء current_user["id"]
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
    return user_dict
