from fastapi import HTTPException, status
from app.models.identity import User

class AuthorizationPolicy:
    @staticmethod
    def verify_capability(user: User, capability_attr: str, error_message: str):
        """التحقق المركزي المشترك من القدرات الحية للمستخدم في قاعدة البيانات"""
        # إذا كان الحساب مشرفاً عاماً (أنت)، يمتلك الصلاحية المطلقة تلقائياً لإدارة النظام وتعيين الموظفين
        if user.is_admin:
            return True
            
        if not getattr(user, capability_attr, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_message
            )
        return True

    @staticmethod
    def can_manage_platform(user: User):
        """القدرة الإدارية العليا لتعديل الاشتراكات، العمولات، وإضافة الموظفين بالخارج"""
        return AuthorizationPolicy.verify_capability(
            user, "is_admin", "عذراً، هذا الإجراء مخصص للمشرف العام على النظام فقط."
        )

    @staticmethod
    def can_moderate_content(user: User):
        """القدرة على مراجعة الإعلانات، إدارة النزاعات والبلاغات"""
        if user.is_admin or user.is_moderator:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، لا تمتلك قدرة مراقبة العمليات والنزاعات."
        )

    @staticmethod
    def can_list_assets(user: User):
        """القدرة على نشر الأصول والمعدات في الـ Marketplace"""
        return AuthorizationPolicy.verify_capability(
            user, "is_seller", "لإتمام هذا الإجراء، يرجى تفعيل قدرة (تاجر/معدن) من لوحة حسابك الموحد أولاً."
        )

    @staticmethod
    def can_use_trade_desk(user: User):
        """القدرة على استخدام مكتب التجارة الدولية ورفع الفواتير (Global Trade Desk)"""
        return AuthorizationPolicy.verify_capability(
            user, "is_importer", "لإتمام هذا الإجراء، يرجى تفعيل قدرة (مستورد) من لوحة حسابك الموحد أولاً."
        )

    @staticmethod
    def can_provide_global_services(user: User):
        """القدرة على رؤية الصفقات وتقديم العروض الدولية (Global Service Provider)"""
        return AuthorizationPolicy.verify_capability(
            user, "is_global_provider", "هذه اللوحة مخصصة فقط لمزودي الخدمات العالميين المعتمدين (Global Service Providers)."
        )
