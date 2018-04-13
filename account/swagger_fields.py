import coreapi


empty_fields = ()

UsersFieldsSwagger = {
    'login': (
        coreapi.Field(
            name='user_type',
            location='form',
            required=False,
            description='user_type',
            type='string'
        ),
        coreapi.Field(
            name='username',
            location='form',
            required=True,
            description='username',
            type='string'
        ),
        coreapi.Field(
            name='password',
            location='form',
            required=True,
            description='Enter valid password',
            type='string'
        )
    ),
    'changePassword': (
        coreapi.Field(
            name='old_password',
            location='form',
            required=False,
            description='old password',
            type='string'
        ),
        coreapi.Field(
            name='password',
            location='form',
            required=True,
            description='password',
            type='string'
        ),
        coreapi.Field(
            name='confirm_password',
            location='form',
            required=True,
            description='confirm password',
            type='string'
        ),
    ),
    'checkDuplicateEmail': (
        coreapi.Field(
            name='email',
            location='query',
            required=True,
            description='check for duplicate Email address.',
            type='string'
        ),
    ),
    'checkDuplicateUsername': (
        coreapi.Field(
            name='username',
            location='query',
            required=True,
            description='check for duplicate Username.',
            type='string'
        ),
    ),
    'resetPassword': (
        coreapi.Field(
            name='email',
            location='query',
            required=True,
            description='check for duplicate Email address.',
            type='string'
        ),
    ),
    'deactivateSubAdmin': (
        coreapi.Field(
            name='email',
            location='query',
            required=True,
            description='check for duplicate Email address.',
            type='string'
        ),
    ),
    'deleteSubAdmin': (
        coreapi.Field(
            name='email',
            location='query',
            required=True,
            description='check for duplicate Email address.',
            type='string'
        ),
    ),
    'faq': (
        coreapi.Field(
            name='user_type',
            location='query',
            required=True,
            description='To retrieve faq according to user_type',
            type='string'
        ),
    )
}
