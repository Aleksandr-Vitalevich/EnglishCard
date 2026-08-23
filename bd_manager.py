from sqlalchemy import create_engine,Column,Integer,String,Numeric,ForeignKey,DECIMAL,DateTime,func
from sqlalchemy.orm import declarative_base,sessionmaker,aliased
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import json
from security import hash_password, check_password, generate_secure_password

Base = declarative_base()

class users(Base) :
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),unique=True, nullable=False)
    password = Column(String(255),nullable=False)
    counter_point = Column(Integer,default=0)
class words(Base) :
    __tablename__ = "words"
    word_id = Column(Integer,primary_key=True,autoincrement=True)
    words_english = Column(String(255),nullable=False)
    words_russian = Column(String(255),nullable=False)
class user_words(Base) :
    __tablename__ = "user_words"
    user_id = Column(Integer,ForeignKey('users.user_id',ondelete="CASCADE"),primary_key=True,nullable=False)
    word_id = Column(Integer,ForeignKey('words.word_id',ondelete="CASCADE"),primary_key=True,nullable=False)
    status = Column(String(50),nullable=False)
class learning_stats(Base) :
    __tablename__ = "learning_stats"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    word_id = Column(Integer,ForeignKey("words.word_id",ondelete="CASCADE"),nullable=False)
    correct_answers = Column(Integer,default=0,nullable=False)
    total_attempts = Column(Integer,default=0,nullable=False)
    last_reviewed = Column(DateTime,default=func.now(),onupdate=func.now())

class BD_MANAGER :
    def __init__(self,user = None, password = None, host = None, port = None, db_name = None):
        DATABAE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        try :
            self.engine = create_engine(DATABAE_URL,echo=True)
            with self.engine.connect() as connection :
                Base.metadata.create_all(self.engine)
                print('Подключение успешно')
            self.Session = sessionmaker(bind=self.engine)
        except SQLAlchemyError as e :
            print(f'Ошибка соединения {e} ')

    def read_file_json(self,path) :
        '''Функция для чтения файлов формата json
        Принимает путь к фвйлу'''
        with open(path,'r',encoding='utf-8') as file :
            file_read = json.load(file)
            return file_read
        
    def add_words_to_bd(self,path) :
        '''Функция наполнения базы данных словами из файла
        Функция принимает путь и передает его в функцию чтения файла
        '''
        try :
            with self.Session() as session :
                words_count = session.query(words).count()
                if words_count > 0 :
                    print("В базе данных уже есть слова из этого файла. Загрузите другой файл")
                    return True
                 
                file = self.read_file_json(path)
                for line in file :
                    new_word = words(
                    words_english = line.get("words_english"),
                    words_russian = line.get("words_russian"),
                    )
                    session.add(new_word)
                session.commit()
            print('Успех, записи успешно добавлены')
            return True
        except SQLAlchemyError as e :
            print(f"Ошибка добавления записи {e}")
            return None

    def add_word_admin(self,english,russian) :
        '''Функция добавления слова админом в бд
        На вход функция принимает два параметра -> str'''
        try :
            with self.Session() as session :
                check_query = session.query(words).filter_by(words_english=english.strip().lower()).first()
                if check_query :
                    print(f'Слово {english} уже есть в базе')
                    return "duplicate"
                
                add_word = words(
                    words_english = english,
                    words_russian = russian,
                ) 
                session.add(add_word)
                session.commit()
                print('Слово успешно добавлено')
            return True
        except SQLAlchemyError as e :
            print(f'Ошибка добавления записи {e}')
            return None

    def add_word_personal(self,user_id,word_id) :
            '''Функция добавления слова пользователем в личный кабинет
            На вход функция принимает два параметра id пользователя -> int, id слова -> int'''
            try :
                with self.Session() as session :
                    check_query = session.query(user_words).filter_by(user_id=user_id,word_id=word_id).first()

                    if check_query :
                        print(f'Слово уже есть в вашем тренажере')
                        return "exists"
                    
                    add_word = user_words(
                        user_id = user_id,
                        word_id = word_id,
                        status = "Изучается",
                    ) 
                    session.add(add_word)
                    session.commit()
                    print('Слово успешно добавлено')
                return True
            except SQLAlchemyError as e :
                print(f'Ошибка добавления записи {e}')
                return None

    def delete_word_admin(self,english = None,russian = None) :
                    '''Функция удаления слова из базы данных
                    На вход функция принимает два параметра -> str
                    Достаточно ввести что-то одно'''
                    try :
                        with self.Session() as session :
                            get_record_word = None
                            if english :
                                get_record_word = session.query(words).filter_by(words_english=english.strip().lower()).first()
                            elif russian :
                                get_record_word = session.query(words).filter_by(words_russian=russian.strip().lower()).first()
                            if not get_record_word :
                                print('Запись не найдена в базе')
                                return "not_found"
                            session.delete(get_record_word)
                            session.commit()
                            print('Слово успешно удалено')
                        return True
                    except SQLAlchemyError as e :
                        print(f'Ошибка удаления записи {e}')
                        return None

    def delete_word_personal(self,user_id,word_id) :
                '''Функция удаления слова из личного кабинета пользователя
                На вход функция принимает два параметра id пользователя -> int, id слова -> int'''
                try :
                    with self.Session() as session :
                        get_record_word = session.query(user_words).filter_by(user_id=user_id,word_id=word_id).first()
                        if not get_record_word :
                            print('Запись не найдена в базе')
                            return "not_found"
                        session.delete(get_record_word)
                        session.commit()
                        print('Слово успешно удалено')
                    return True
                except SQLAlchemyError as e :
                    print(f'Ошибка удаления записи {e}')
                    return None

    def change_status(self,user_id,word_id,status) :
        '''Функция изменения статуса
        На вход функция принимает три параметра id пользователя -> int, id слова -> int, status -> str'''
        try :
            with self.Session() as session :
                get_record = session.query(user_words).filter_by(user_id=user_id,word_id=word_id).first()
                if not get_record :
                    print(f'Запись не найдена')
                    return False
                get_record.status = status
                session.commit()
                print(f'Статус изменен на {status}')
            return True
        except SQLAlchemyError as e :
            print(f'Ошибка изменения статуса {e}')
            return None

    def add_user(self,name,password) :
        '''Функция добавления нового пользователя
        На вход функция принимает два параметра 
        name - имя пользователя -> str, 
        password - пароль -> int
        Функция проверяет наличие пользователей в бд , 
        если пользователей нет создается автоматически первый пользователь root
        Если пользователь в базе есть возвращается сообщение о том что пользователь в базе есть'''
        try :
            with self.Session() as session :
                query_check_base = session.query(users).count()
                if query_check_base == 0 :
                    root_password = generate_secure_password()
                    hash_root_password = hash_password(root_password)

                    add_root = users(
                        name = "root",
                        password = hash_root_password,
                    )
                    session.add(add_root)
                    session.commit()
                    print("\n" + "="*25)
                    print(f'Пользователь root добавлен в базу ')
                    print(f"Пароль для входа {root_password}")
                    print(f"Обязательно скопируйте его")
                    print("\n" + "="*25)


                clear_name = name.strip().lower()
                query_check = session.query(users).filter_by(name=clear_name).first()

                if query_check :
                    print(f'Пользователь {clear_name} уже есть в базе')
                    return 'exists'

                hash_user_password = hash_password(password.strip())

                new_user = users(
                    name = clear_name,
                    password = hash_user_password,
                )
                session.add(new_user)
                session.commit()
                print(f'Пользователь {name} добавлен в базу ')
            return True
        except SQLAlchemyError as e :
            print(f'Ошибка добавления записи {e}')
            return None

    def delete_user_admin(self,user_name=None,user_id=None) :
        '''Функция удаления пользователя
        На вход функция принимает два параметра user_name -> имя пользователя,
        id пользователя -> int
        Достаточно ввести что-то одно'''
        try :
            with self.Session() as session :
                get_record = None
                if user_name :
                    get_record = session.query(users).filter_by(name=user_name.strip().lower()).first()
                elif user_id :
                    get_record = session.query(users).filter_by(user_id=user_id).first()
                if not get_record :
                    print('Пользователь не найден в базе')
                    return None
                session.delete(get_record)
                session.commit()
                print(f'Пользователь успешно удален')
            return True
        except SQLAlchemyError as e :
            print(f'Ошибка удаления пользователя {e}')
            return None

    def get_authorization(self,name,password) :
        '''Функция авторизации
        На вход функция принимает два параметра name - имя пользователя -> str,
        password - пароль -> int'''
        try :
            with self.Session() as session :
                query_check = session.query(users).filter_by(name=name.strip().lower()).first()
                if not query_check :
                    print('Пользователь не найден в базе')
                    return None
                if check_password(password.strip(),query_check.password) :
                    print(f'Добро пожаловать {name}')
                    return query_check
                else :
                    print("Неверный пароль")
                    return None
        except SQLAlchemyError as e :
            print(f'Ошибка авторизации {e}')
            return None

    def get_card_random(self,user_id) :
        '''Функция получения случайного слова
        На вход функция получает user_id id - пользователя -> int'''
        try :
            with self.Session() as session :
                get_word = session.query(words).join(user_words).filter(user_words.user_id == user_id,user_words.status == "Изучается").order_by(func.random()).first()
                if not get_word :
                    get_word = session.query(words).order_by(func.random()).first()
                if not get_word :
                    print('Нет слов для изучения')
                    return "empty"
                print(f'Получено слово {get_word.words_english}')
                return get_word
        except SQLAlchemyError as e:
            print(f'Ошибка получения данных {e}')
            return None

    def get_wrong_choise(self,correct_translation : str) :
        '''Получение 3х неправильных слов , нужно для режима тест
        Функция принимает перевод слова , чтобы не получить два или более одинаковых слов в выборке'''
        try :
            with self.Session() as session :
                wrong_words_query = session.query(words).filter(words.words_russian != correct_translation).order_by(func.random()).limit(3).all()
                return [word.words_english for word in wrong_words_query]
        except SQLAlchemyError as e :
            print(f'Ошибка получения данных {e}')
            return []

    def get_and_update_status(self, user_id: int, word_id: int, is_correct: bool):
        '''Функция обновления данных по прогрессу изучения слов
        Если пользователь правильно ответит на слово 3 раза статус автоматически изменится'''
        try:
            with self.Session() as session:
                if is_correct:
                    user_record = session.query(users).filter_by(user_id=user_id).first()
                    if user_record:
                        user_record.counter_point += 1

                stat_record = session.query(learning_stats).filter_by(user_id=user_id, word_id=word_id).first()
                
                if not stat_record:
                    stat_record = learning_stats(user_id=user_id, 
                                                 word_id=word_id,
                                                 total_attempts=0,
                                                 correct_answers=0)
                    session.add(stat_record)
                if stat_record.total_attempts is None:
                    stat_record.total_attempts = 0
                if stat_record.correct_answers is None:
                    stat_record.correct_answers = 0
                stat_record.total_attempts += 1
                if is_correct:
                    stat_record.correct_answers += 1

                if stat_record.correct_answers >= 3:
                    user_word_record = session.query(user_words).filter_by(user_id=user_id, word_id=word_id).first()
                    if user_word_record and user_word_record.status == "Изучается":
                        user_word_record.status = "Изучено"
                        print(f"Карточка с ID {word_id} изучена")

                session.commit()
                print(f"Изменен статус по слову с id {word_id}")
            return True
        except SQLAlchemyError as e:
            print(f'Ошибка связи: {e}')
            return None

    def get_user_words(self,user_id,status) :
        '''Функция получения слов пользователя из базы данных'''
        try :
            with self.Session() as session :
                get_query = session.query(words).join(
                    user_words,
                    words.word_id == user_words.word_id).filter(
                        user_words.user_id == user_id,
                        user_words.status == status).all()
                return get_query
        except SQLAlchemyError as e :
            print(f"Ошибка получения слов {e}")
            return None

    def get_points(self,user_id) :
        '''Функция получения очков пользователя'''
        try :
            with self.Session() as session :
                user_point = session.query(users).filter_by(user_id=user_id).first()
                if user_point :
                    return user_point.counter_point
                return 0
        except SQLAlchemyError as e :
            print(f"Ошибка выполнения запроса {e}")
            return 0

    def get_user_stats(self,user_id) :
        '''Функция получения ответов пользователя по словам'''
        try :
            with self.Session() as session :
                query = session.query(
                    words.words_english,
                    learning_stats.correct_answers.label("Правильные ответы "),
                    learning_stats.total_attempts.label("Всего попыток "),
                    learning_stats.last_reviewed.label("Последняя попытка ")).join(
                        learning_stats,words.word_id == learning_stats.word_id
                    ).filter(learning_stats.user_id == user_id).all()
                return query
        except SQLAlchemyError as e :
            print(f"Ошибка выполнения запроса {e}")
            return []
        
    def get_users_admin(self) :
        '''Функция получения списка пользователей'''
        try :
            with self.Session() as session :
                query_get_users = session.query(
                    users.user_id.label("id Пользователя"),
                    users.name.label("Ник пользователя")).all()
                return query_get_users
        except SQLAlchemyError as e :
            print(f"Ошибка выполнения запроса {e}")
            return []