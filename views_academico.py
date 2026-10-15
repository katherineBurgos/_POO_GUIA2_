from models_academico import Estudiante, Docente, Materia, Matricula
from views import CrudBase
from shared.json_manager import GestorJSON



class CrudAcademicoMixin:
    def guardar(self):
        self.gestor.guardar([obj.a_diccionario() for obj in self.lista])
    def leer(self):
        return self.lista
    def buscar(self, texto):
        t = str(texto).strip().lower()
        return [obj for obj in self.lista if t and any(t in str(getattr(obj, c, "")).lower() for c in self.CAMPOS_BUSCABLES)]
    def siguiente(self):
        return max((obj.id for obj in self.lista), default=0) + 1
    def obtener(self, identificador):
        return next((obj for obj in self.lista if obj.id == int(identificador)), None)
    def existe(self, identificador):
        return self.obtener(identificador) is not None
    def registros(self):
        return [obj.a_diccionario() for obj in self.lista]
    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        try:
            obj = self.MODELO(self.siguiente(), **{k:v for k,v in datos.items() if k in self.MODELO.CAMPOS})
        except (ValueError, TypeError) as exc: return False, str(exc)
        self.lista.append(obj); self.guardar()
        return True, f"{self.NOMBRE.capitalize()} creado"
    def actualizar(self, identificador, cambios):
        obj = self.obtener(identificador)
        if obj is None: return False, f"No existe {self.NOMBRE}"
        datos = obj.a_diccionario(); datos.update(cambios)
        error = self.validar(datos, id_actual=int(identificador))
        if error: return False, error
        try: nuevo = self.MODELO.desde_diccionario(datos)
        except (ValueError, TypeError) as exc: return False, str(exc)
        self.lista[self.lista.index(obj)] = nuevo; self.guardar()
        return True, f"{self.NOMBRE.capitalize()} actualizado"
    def eliminar(self, identificador):
        obj = self.obtener(identificador)
        if obj is None: return False, f"No existe {self.NOMBRE}"
        self.lista.remove(obj); self.guardar()
        return True, f"{self.NOMBRE.capitalize()} eliminado"

class EstudianteController(CrudAcademicoMixin, CrudBase):

    def __init__(self, archivo=None):
        self.nombre = self.NOMBRE
        self.campos = self.MODELO.CAMPOS
        self.gestor = GestorJSON(archivo or self.ARCHIVO)
        self.lista = [self.MODELO.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([obj.a_diccionario() for obj in self.lista])

    def leer(self):
        return self.lista

    def buscar(self, texto):
        t = str(texto).strip().lower()
        return [obj for obj in self.lista if t and any(t in str(getattr(obj, c, "")).lower() for c in self.CAMPOS_BUSCABLES)]

    def siguiente(self):
        return max((obj.id for obj in self.lista), default=0) + 1

    def obtener(self, identificador):
        return next((obj for obj in self.lista if obj.id == int(identificador)), None)

    def existe(self, identificador):
        return self.obtener(identificador) is not None

    def registros(self):
        return [obj.a_diccionario() for obj in self.lista]

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        try:
            obj = self.MODELO(self.siguiente(), **{k: v for k, v in datos.items() if k in self.MODELO.CAMPOS})
        except (ValueError, TypeError) as exc:
            return False, str(exc)
        self.lista.append(obj); self.guardar()
        return True, f"{self.NOMBRE.capitalize()} creado"

    def actualizar(self, identificador, cambios):
        obj = self.obtener(identificador)
        if obj is None: return False, f"No existe {self.NOMBRE}"
        datos = obj.a_diccionario(); datos.update(cambios)
        error = self.validar(datos, id_actual=int(identificador))
        if error: return False, error
        try:
            nuevo = self.MODELO.desde_diccionario(datos)
        except (ValueError, TypeError) as exc:
            return False, str(exc)
        self.lista[self.lista.index(obj)] = nuevo; self.guardar()
        return True, f"{self.NOMBRE.capitalize()} actualizado"

    def eliminar(self, identificador):
        obj = self.obtener(identificador)
        if obj is None: return False, f"No existe {self.NOMBRE}"
        self.lista.remove(obj); self.guardar()
        return True, f"{self.NOMBRE.capitalize()} eliminado"

    """LISTO como ejemplo: cópialo y guíate con él para los demás."""

    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"
    NOMBRE = "estudiante"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS
                         if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if "carnet" in datos and str(datos["carnet"]).strip():
            carnet = str(datos["carnet"]).strip().upper()
            usados = {r["carnet"].upper() for r in self.registros()
                      if r["id"] != id_actual}
            if carnet in usados:
                return f"El carnet {carnet} ya está registrado"
        return None


class DocenteController(CrudAcademicoMixin, CrudBase):

    def __init__(self, archivo=None):
        self.nombre = self.NOMBRE
        self.campos = self.MODELO.CAMPOS
        self.gestor = GestorJSON(archivo or self.ARCHIVO)
        self.lista = [self.MODELO.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([obj.a_diccionario() for obj in self.lista])

    def leer(self):
        return self.lista

    def buscar(self, texto):
        t = str(texto).strip().lower()
        return [obj for obj in self.lista if t and any(t in str(getattr(obj, c, "")).lower() for c in self.CAMPOS_BUSCABLES)]

    def siguiente(self):
        return max((obj.id for obj in self.lista), default=0) + 1

    def obtener(self, identificador):
        return next((obj for obj in self.lista if obj.id == int(identificador)), None)

    def existe(self, identificador):
        return self.obtener(identificador) is not None

    def registros(self):
        return [obj.a_diccionario() for obj in self.lista]

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        try:
            obj = self.MODELO(self.siguiente(), **{k: v for k, v in datos.items() if k in self.MODELO.CAMPOS})
        except (ValueError, TypeError) as exc:
            return False, str(exc)
        self.lista.append(obj); self.guardar()
        return True, f"{self.NOMBRE.capitalize()} creado"

    def actualizar(self, identificador, cambios):
        obj = self.obtener(identificador)
        if obj is None: return False, f"No existe {self.NOMBRE}"
        datos = obj.a_diccionario(); datos.update(cambios)
        error = self.validar(datos, id_actual=int(identificador))
        if error: return False, error
        try:
            nuevo = self.MODELO.desde_diccionario(datos)
        except (ValueError, TypeError) as exc:
            return False, str(exc)
        self.lista[self.lista.index(obj)] = nuevo; self.guardar()
        return True, f"{self.NOMBRE.capitalize()} actualizado"

    def eliminar(self, identificador):
        obj = self.obtener(identificador)
        if obj is None: return False, f"No existe {self.NOMBRE}"
        self.lista.remove(obj); self.guardar()
        return True, f"{self.NOMBRE.capitalize()} eliminado"

    MODELO = Docente
    ARCHIVO = "data/docentes.json"
    NOMBRE = "docente"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "especialidad")

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"
        email = str(datos.get("email", "")).strip().lower()
        if email:
            usados = {r["email"].lower() for r in self.registros() if r["id"] != id_actual}
            if email in usados:
                return f"El email {email} ya está registrado"
        return None


class MateriaController(CrudAcademicoMixin, CrudBase):
    MODELO = Materia
    ARCHIVO = "data/materias.json"
    NOMBRE = "materia"
    CAMPOS_BUSCABLES = ("nombre", "codigo")

    def __init__(self, docentes=None):
        self.docentes = docentes or DocenteController()
        self.nombre = self.NOMBRE
        self.campos = self.MODELO.CAMPOS
        self.gestor = GestorJSON(self.ARCHIVO)
        self.lista = [self.MODELO.desde_diccionario(d) for d in self.gestor.leer()]

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"
        codigo = str(datos.get("codigo", "")).strip().upper()
        if codigo:
            usados = {r["codigo"].upper() for r in self.registros() if r["id"] != id_actual}
            if codigo in usados:
                return f"El código {codigo} ya está registrado"
        docente_id = datos.get("docente_id")
        if docente_id not in (None, ""):
            try:
                if not self.docentes.existe(int(docente_id)):
                    return f"No existe el docente {docente_id}"
            except (ValueError, TypeError):
                return "docente_id debe ser un número válido"
        return None

    def asignar_docente(self, materia_id, docente_id):
        if not self.existe(int(materia_id)):
            return "No existe la materia"
        if not self.docentes.existe(int(docente_id)):
            return "No existe el docente"
        return self.actualizar(int(materia_id), {"docente_id": int(docente_id)})

    def materias_de_docente(self, docente_id):
        return [m for m in self.listar() if m.docente_id == docente_id]


class MatriculaController(CrudAcademicoMixin, CrudBase):
    """El equivalente académico del VentaController."""

    MODELO = Matricula
    ARCHIVO = "data/matriculas.json"
    NOMBRE = "matrícula"
    CAMPOS_BUSCABLES = ("periodo",)

    def __init__(self, estudiantes=None, materias=None):
        self.estudiantes = estudiantes or EstudianteController()
        self.materias = materias or MateriaController()
        self.nombre = self.NOMBRE
        self.campos = self.MODELO.CAMPOS
        self.gestor = GestorJSON(self.ARCHIVO)
        self.lista = [self.MODELO.desde_diccionario(d) for d in self.gestor.leer()]

    def validar(self, datos, id_actual=None):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (ValueError, TypeError):
            return "Los identificadores de estudiante y materia deben ser números"
        if not self.estudiantes.existe(estudiante_id):
            return f"No existe el estudiante {estudiante_id}"
        if not self.materias.existe(materia_id):
            return f"No existe la materia {materia_id}"
        periodo = str(datos.get("periodo", "")).strip()
        for r in self.registros():
            if r["id"] != id_actual and int(r.get("estudiante_id", 0)) == estudiante_id and int(r.get("materia_id", 0)) == materia_id and r.get("periodo", "") == periodo:
                return "El estudiante ya está matriculado en esa materia durante ese periodo"
        return None

    def agregar_nota(self, matricula_id, tipo, valor, peso=1):
        matricula = self.obtener(int(matricula_id))
        if matricula is None:
            return "No existe la matrícula"
        try:
            matricula.agregar_nota(tipo, float(valor), float(peso))
        except (ValueError, TypeError) as exc:
            return str(exc)
        return self._guardar_objeto(matricula)

    def boletin(self, estudiante_id):
        matriculas = [m for m in self.leer() if m.estudiante_id == int(estudiante_id)]
        if not matriculas:
            return f"No hay matrículas para el estudiante {estudiante_id}"
        lineas = [f"BOLETÍN DEL ESTUDIANTE #{estudiante_id}", "=" * 48]
        promedios = []
        for m in matriculas:
            materia = self.materias.obtener(m.materia_id)
            nombre = materia.nombre if materia else f"Materia #{m.materia_id}"
            lineas.append(f"{nombre} | {m.periodo} | Promedio: {m.promedio} | Estado: {m.estado}")
            if m.promedio is not None:
                promedios.append(float(m.promedio))
        lineas.append("-" * 48)
        lineas.append(f"Promedio general: {sum(promedios)/len(promedios):.2f}" if promedios else "Promedio general: sin notas")
        return "\n".join(lineas)