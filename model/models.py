import json
from datetime import datetime
from typing import Optional, Type
from sqlalchemy import DateTime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接
DATABASE_URL = "sqlite:///AIQA.db"  # SQLite 数据库
engine = create_engine(DATABASE_URL, echo=True)

# 基类
Base = declarative_base()
# 创建 Session
SessionLocal = sessionmaker(bind=engine)


def InitDB():
    # 创建所有表
    Base.metadata.create_all(engine)


# DAO 基类,这倒是很新奇的做法,没玩过,没有gorm包装的那么好,不是很方便但是封装自由度还是很高的
class BaseDAO:
    def __init__(self):
        self.session = SessionLocal()

    def save(self, obj: Base):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: Base):
        self.session.delete(obj)
        self.session.commit()


# 用户表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stdID = Column(String, unique=True, nullable=False)
    place = Column(String, nullable=False)


# 用户 DAO
class UserDAO(BaseDAO):
    def first_or_create(self, stdID: str, place: str) -> User:
        user = self.session.query(User).filter_by(stdID=stdID).first()
        if not user:
            user = User(stdID=stdID, place=place)
            self.save(user)
        return user


# 问题表
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    options = Column(Text, nullable=False)  # JSON 字符串
    answer = Column(String, nullable=False)


# 问题 DAO
class QuestionDAO(BaseDAO):
    def save_question(self, content: str, options: dict, answer: str) -> Optional[Question]:
        content = content.strip()
        op = json.dumps(options)
        """
        保存问题，增加去重功能：如果相同 content 的问题已存在，则不重复存储。
        """
        # 检查是否存在重复的问题
        existing_question = (
            self.session.query(Question)
            .filter_by(content=content, options=op)
            .first()
        )

        if existing_question:
            return None  # 返回 None 表示没有存储新问题

        # 存储新问题
        question = Question(content=content, options=op, answer=answer)
        return self.save(question)

    def find_question(self, question_id: int) -> Optional[Type[Question]]:
        return self.session.query(Question).filter_by(id=question_id).first()

    def get_total(self) -> int:
        return self.session.query(Question).count()


# 答案表
class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stdID = Column(String, nullable=False)
    questionID = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    start = Column(DateTime, nullable=False)  # 修改为 DateTime 类型
    end = Column(DateTime, nullable=False)  # 修改为 DateTime 类型
    answer = Column(String, nullable=False)


# 答案 DAO
class AnswerDAO(BaseDAO):
    def find(self, stdID: str, questionID: int) -> Optional[Type[Answer]]:
        ans = self.session.query(Answer).filter_by(stdID=stdID, questionID=questionID).first()
        return ans

    def first_or_create(self, stdID: str, questionID: int, status: bool, start: str, end: str, answer: str) -> Answer:
        # 将字符串转换为 datetime 对象
        def parse_datetime(value: str) -> datetime:
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  # 指定字符串格式
            except ValueError:
                raise ValueError(f"Invalid datetime format: {value}")

        # 转换 start 和 end 字段
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)

        ans = self.session.query(Answer).filter_by(stdID=stdID, questionID=questionID).first()
        if not ans:
            ans = Answer(
                stdID=stdID,
                questionID=questionID,
                status=status,
                start=start_dt,  # 使用转换后的 datetime 对象
                end=end_dt,  # 使用转换后的 datetime 对象
                answer=answer
            )
            self.save(ans)
        return ans

    def find_latest(self, stdID: str) -> int:

        answer = self.session.query(Answer).filter_by(stdID=stdID).order_by(Answer.id.desc()).first()
        if answer != None:
            return answer.questionID
        else:
            return 0

    def countRight(self, stdID: str) -> int:
        return self.session.query(Answer).filter_by(status=True, stdID=stdID).count()

    def calculate_time_spent_str(self, answer_id: int) -> Optional[str]:

        answer = self.session.query(Answer).filter_by(id=answer_id).first()
        if answer:
            time_spent = answer.end - answer.start
            # 格式化为 HH:mm:ss
            hours, remainder = divmod(time_spent.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        return f"{0:02}:{0:02}:{0:02}"
