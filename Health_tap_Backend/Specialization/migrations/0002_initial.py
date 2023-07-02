from django.db import migrations

insert_sql = """
INSERT INTO "Specialization_specialization" ("id", "name") VALUES
(1, 'دكتور جراحة'),
(2, 'دكتور طب القلب'),
(3, 'دكتور أمراض الجلد'),
(4, 'دكتور غدد صماء'),
(5, 'دكتور أمراض الجهاز الهضمي'),
(6, 'دكتور أمراض الدم'),
(7, 'دكتور أمراض الأعصاب'),
(8, 'دكتور أمراض السرطان'),
(9, 'دكتور العظام والمفاصل'),
(10, 'دكتور طب الأطفال'),
(11, 'دكتور طب النفسي'),
(12, 'دكتور طب الأسنان'),
(13, 'دكتور طب العيون'),
(14, 'دكتور طب الأذن والحنجرة'),
(15, 'دكتور طب النساء والتوليد'),
(16, 'دكتور طب التخدير'),
(17, 'دكتور طب الأورام'),
(18, 'دكتور طب الأمراض المعدية'),
(19, 'دكتور طب الجهاز التنفسي'),
(20, 'دكتور طب الجهاز البولي'),
(21, 'دكتور طب الغدد الدرقية'),
(22, 'دكتور طب الأمراض النفسية'),
(23, 'دكتور طب الأعشاب الطبية'),
(24, 'دكتور طب الأسنان العام'),
(25, 'دكتور طب الأسنان الترميمي'),
(26, 'دكتور طب الأسنان التقويمي'),
(37, 'دكتور طب الأسنان الجراحي');
"""

class Migration(migrations.Migration):
    initial = True
    dependencies = [        ('Specialization', '0001_initial'),    ]

    operations = [        migrations.RunSQL(insert_sql),    ]