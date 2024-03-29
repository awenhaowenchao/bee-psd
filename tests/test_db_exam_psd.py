from bee_psd import Psd, CX, On, T
from bee_psd import Model, IntegerField, StringField, DateTimeField, Equal, W, C
import logging

logging.basicConfig(level=logging.DEBUG)

db_exam = Psd.open("exam")
# 1) sing table count search, SELECT COUNT(*) AS COUNT FROM t_teacher
with db_exam.connection() as conn:
    teacher_count = db_exam.select(CX("COUNT(*)", "COUNT")).From("t_teacher").int()
    print("total techer count is %s" % teacher_count)

# 2) sing table search, SELECT * FROM t_teacher
with db_exam.connection() as conn:
    teachers = db_exam.select(CX("*")).From("t_teacher").list()
    print(teachers)

# 3) sing table search, SELECT * FROM t_teacher convert values to model of Teacher
class Teacher(Model):
    __table__ = 't_teacher'

    id = IntegerField(primary_key=True)
    name = StringField()

with db_exam.connection() as conn:
    teachers = db_exam.select(CX("*")).From("t_teacher").list(Teacher)
    print(teachers)

# 4) sing table search, SELECT * FROM t_teacher WHERE id=? convert values to model of Teacher
with db_exam.connection() as conn:
    teachers = db_exam.select(CX("*")).From("t_teacher").Where(W().equal("id", 1004)).list(Teacher)
    print(teachers)

# 5) tow table Join search, SELECT DISTINCT id,cid,score FROM t_student JOIN t_sc ON id=sid WHERE id=?
with db_exam.connection() as conn:
    result = db_exam.query(C("id", "cid", "score"), True)\
        .From("t_student")\
        .Join("t_sc", On("id", "sid"))\
        .Where(Equal("id", 1001))\
        .list()
    print(result)

#or use alias mode like 'SELECT DISTINCT s.id,sc.cid,sc.score FROM t_student AS s JOIN t_sc AS sc ON s.id=sc.sid WHERE s.id=?'

with db_exam.connection() as conn:
    result = db_exam.query(C("s.id", "sc.cid", "sc.score"), True)\
        .From(T("t_student", "s"))\
        .Join(T("t_sc", "sc"), On("s.id", "sc.sid"))\
        .Where(Equal("s.id", 1001))\
        .list()
    print(result)

# 6) with transaction
with db_exam.transaction():
    # insert sql
    # update sql
    # raise exception
    # update Sql
    pass


# 7) sing table search, SELECT * FROM t_student limit 0, 5
with db_exam.connection() as conn:
    students = db_exam.select(CX("*")).From("t_student").limit(1, 5).list()
    print(students)






