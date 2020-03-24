CATEGORY_TYPE = (
    ('DATA', 'data'),
    ('ENUM', 'enum'),
)

PLAN_TYPE = (
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('professional', 'Professional'),
)

FIELD_TYPE = (
    ("foreignkey", "models.ForeignKey"),
    ("auto", "models.AutoField"),
    ("bigauto", "models.BigAutoField"),
    ("biginteger", "models.BigIntegerField"),
    ("binary", "models.BinaryField"),
    ("boolean", "models.BooleanField"),
    ("char", "models.CharField"),
    ("date", "models.DateField"),
    ("datetime", "models.DateTimeField"),
    ("email", "models.EmailField"),
    ("file", "models.Field"),
    ("float", "models.FloatField"),
    ("int", "models.IntegerField"),
    ("text", "models.TextField"),
    ("uuid", "models.UUIDField"),
    ("commaseparatedinteger", "models.CommaSeparatedIntegerField"),
    ("decimal", "models.DecimalField"),
    ("duration", "models.DurationField"),
    ("filepath", "models.FilePathField"),
    ("image", "models.ImageField"),
    ("genericipaddress", "models.GenericIPAddressField"),
    ("nullbool", "models.NullBooleanField"),
    ("positiveinteger", "models.PositiveIntegerField"),
    ("positivesmallinteger", "models.PositiveSmallIntegerField"),
    ("slug", "models.SlugField"),
    ("smallinteger", "models.SmallIntegerField"),
    ("time", "models.TimeField"),
    ("url", "models.URLField"),
)
