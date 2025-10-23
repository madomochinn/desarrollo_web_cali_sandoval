from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from sqlalchemy import func, Date, extract
from datetime import datetime

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()



class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    region = relationship("Region", back_populates="comunas")
    avisos = relationship("AvisoAdopcion", back_populates="comuna")

class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    
    fecha = Column(DateTime, nullable=False, default=datetime.now) 
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)
    
    aviso = relationship("AvisoAdopcion", back_populates="comentarios")

class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    tipo = Column(Enum('gato', 'perro'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm'), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text(500))
    
    comuna = relationship("Comuna", back_populates="avisos")
    fotos = relationship("Foto", back_populates="aviso")
    contactos = relationship("ContactarPor", back_populates="aviso")

    comentarios = relationship("Comentario", order_by="Comentario.fecha.desc()", back_populates="aviso")

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'))
    aviso = relationship("AvisoAdopcion", back_populates="fotos")

class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'))
    aviso = relationship("AvisoAdopcion", back_populates="contactos")


# --- funcioneees ---

def get_session():
    return SessionLocal()

def get_regiones():
    session = get_session()
    regiones = session.query(Region).order_by(Region.id).all()
    session.close()
    return regiones

def get_comunas_by_region(region_id):
    session = get_session()
    comunas = session.query(Comuna).filter_by(region_id=region_id).order_by(Comuna.nombre).all()
    session.close()
    return comunas

def get_comuna_by_id(comuna_id):
    session = get_session()
    comuna = session.query(Comuna).filter_by(id=comuna_id).first()
    session.close()
    return comuna

def create_aviso_adopcion(fecha_ingreso, comuna_id, sector, nombre, email, celular, 
                         tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    session = get_session()
    aviso = AvisoAdopcion(
        fecha_ingreso=fecha_ingreso,
        comuna_id=comuna_id,
        sector=sector,
        nombre=nombre,
        email=email,
        celular=celular,
        tipo=tipo,
        cantidad=cantidad,
        edad=edad,
        unidad_medida=unidad_medida,
        fecha_entrega=fecha_entrega,
        descripcion=descripcion
    )
    session.add(aviso)
    session.commit()
    aviso_id = aviso.id
    session.close()
    return aviso_id

def create_contacto_por(nombre, identificador, aviso_id):
    session = get_session()
    contacto = ContactarPor(nombre=nombre, identificador=identificador, aviso_id=aviso_id)
    session.add(contacto)
    session.commit()
    session.close()

def create_foto(ruta_archivo, nombre_archivo, aviso_id):
    session = get_session()
    foto = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, aviso_id=aviso_id)
    session.add(foto)
    session.commit()
    session.close()

def get_avisos_recientes(limit=5):
    session = get_session()
    avisos = session.query(AvisoAdopcion).options(joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region)).order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(limit).all()
    session.close()
    return avisos

def get_avisos_paginados(offset=0, limit=5):
    session = get_session()
    avisos = session.query(AvisoAdopcion).options(joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region)).order_by(AvisoAdopcion.fecha_ingreso.desc()).offset(offset).limit(limit).all()
    session.close()
    return avisos

def get_total_avisos():
    session = get_session()
    total = session.query(AvisoAdopcion).count()
    session.close()
    return total

def get_aviso_by_id(aviso_id):
    session = get_session()
    aviso = session.query(AvisoAdopcion).options(joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region)).filter(AvisoAdopcion.id == aviso_id).first()
    session.close()
    return aviso

def get_contactos_by_aviso_id(aviso_id):
    session = get_session()
    contactos = session.query(ContactarPor).filter_by(aviso_id=aviso_id).all()
    session.close()
    return contactos

def get_fotos_by_aviso_id(aviso_id):
    session = get_session()
    fotos = session.query(Foto).filter_by(aviso_id=aviso_id).all()
    session.close()
    return fotos

def get_foto_by_id(foto_id):
    session = get_session()
    foto = session.query(Foto).filter_by(id=foto_id).first()
    session.close()
    return foto

def get_avisos_por_dia():
    session = get_session()
    try:
        resultados = session.query(
            func.date(AvisoAdopcion.fecha_ingreso).label('dia'),
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(
            func.date(AvisoAdopcion.fecha_ingreso)
        ).order_by('dia').all()
        
        datos = [{'date': str(resultado.dia), 'count': resultado.cantidad} for resultado in resultados]
        return datos
    except Exception as e:
        print(f"ERROR en get_avisos_por_dia: {str(e)}")
        return []
    finally:
        session.close()

def get_avisos_por_tipo():
    session = get_session()
    try:
        resultados = session.query(
            AvisoAdopcion.tipo,
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(AvisoAdopcion.tipo).all()
        
        datos = [{'tipo': resultado.tipo, 'count': resultado.cantidad} for resultado in resultados]
        return datos
    except Exception as e:
        print(f"ERROR en get_avisos_por_tipo: {str(e)}")
        return []
    finally:
        session.close()

def get_avisos_por_mes():
    session = get_session()
    try:
        resultados = session.query(
            extract('year', AvisoAdopcion.fecha_ingreso).label('año'),
            extract('month', AvisoAdopcion.fecha_ingreso).label('mes'),
            AvisoAdopcion.tipo,
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(
            extract('year', AvisoAdopcion.fecha_ingreso),
            extract('month', AvisoAdopcion.fecha_ingreso),
            AvisoAdopcion.tipo
        ).order_by('año', 'mes', 'tipo').all()
        
        datos = []
        for resultado in resultados:
            datos.append({
                'año': int(resultado.año),
                'mes': int(resultado.mes),
                'tipo': resultado.tipo,
                'count': resultado.cantidad
            })
        return datos
    except Exception as e:
        print(f"ERROR en get_avisos_por_mes: {str(e)}")
        return []
    finally:
        session.close()

def get_comentarios_by_aviso_id(aviso_id):
    session = get_session()
    try:
        # se obtienen y ordenan por fecha descendente (los más nuevos primero)
        comentarios = session.query(Comentario)\
            .filter(Comentario.aviso_id == aviso_id)\
            .order_by(Comentario.fecha.desc())\
            .all()
        return comentarios
    except Exception as e:
        print(f"ERROR al obtener comentarios: {str(e)}")
        return []
    finally:
        session.close()

def save_comentario(aviso_id, nombre, texto):
    session = get_session()
    try:
        nuevo_comentario = Comentario(
            aviso_id=aviso_id,
            nombre=nombre,
            texto=texto,
        )
        session.add(nuevo_comentario)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"ERROR al guardar comentario: {str(e)}")
        raise
    finally:
        session.close()