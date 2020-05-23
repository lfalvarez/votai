THEME=None
POSSIBLE_GENERATING_AREAS_FILTER = 'Comuna'
FILTERABLE_AREAS_TYPE = ['Comuna']
## No muestres las areas en el wizard de creación de propuestas
DONT_SHOW_AREAS_IN_PROPOSAL_WIZARD = True
LIST_ONLY_COMMITED_CANDIDATES = False
#Este es el candidato que aparece enel landing
IMPORTANT_CANDIDATE_IN_LANDING = None
DEFAULT_EXTRAPAGES_FOR_ORGANIZATIONS=[{'title':u'Agenda', 'content':'''* **19 DE NOVIEMBRE**\r\nPrimera vuelta de Elecciones Presidenciales y Parlamentarias
* **17 DE DICIEMBRE**   *Segunda vuelta de Elecciones Presidenciales'''},
                                                           {'title':u'Documentos', 'content':''}]

EXCLUDED_PROPOSALS_APPS = []

PRIORITY_CANDIDATES = []

NOTIFY_CANDIDATES_WHEN_MANY_PROPOSALS_REACH_A_NUMBER = True
WHEN_TO_NOTIFY = [25, 50, 100, 150, 200]
NOTIFY_CANDIDATES = True
NOTIFY_CANDIDATES_OF_NEW_PROPOSAL = True
ORGANIZATION_TEMPLATES_USING_HBS=True
MODERATION_ENABLED=False
HOW_OFTEN_PROPOSAL_REPORTS_ARE_SENT=7
SHARED_PROPOSAL_IMAGE_ID_COLOR = (122,183,255,255)
MEDIA_NARANJA_QUESTIONS_ENABLED=True
ORGANIZATIONS_IN_12_RESULT = True
RECOMMENDED_ORGS_FROM_CACHE = True
SECOND_ROUND_ELECTION = None

MAX_AMOUNT_OF_MAILS_TO_CANDIDATE = 3

DEFAULT_CANDIDATE_EXTRA_INFO = {
    "portrait_photo": "/static/img/candidate-default.jpg",
    "custom_ribbon": "ribbon text"
}
DEFAULT_ELECTION_EXTRA_INFO = {
    "extra": "Extra extra extra"
}
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__),'..', 'whoosh_index'),
    },
}

CACHE_MINUTES = 60

##
CONSTANCE_CONFIG = {
    'SOUL_MATE_INFO_ABOUT_CANDIDATES_MINUTES':(0,'Duracion cache media naranja'),
    'ORGANIZATIONS_MUST_AGREE_TAC_ON_REGISTER':(False,'Organizaciones deben tener terminos y condiciones al registrarse?'),
    'INFINITE_CACHE':(1440,'Tiempo Cache'),
    'DEFAULT_AREA': ('chile', u'El territorio que mostramos por defecto'),
    'AREAS_ARE_FORCED_IN_PROPOSALS' : (False, u'No te preguntamos por el territorio de la propuesta y asumimos que es el que viene por defecto'),
    'PROPOSALS_ENABLED' : (True, 'Habilitar propuestas'),
    'WHEN_TO_NOTIFY': ('25, 50, 100, 150, 200', 'Cuando notificar'),
    'NOTIFY_CANDIDATES': (True, 'Notificar a los candidatos'),
    'NOTIFY_STAFF_OF_NEW_COMMITMENT': (True, 'Notificar al staff si es que hay un nuevo compromiso'),
    'NOTIFY_CANDIDATES_OF_NEW_PROPOSAL': (True, 'Notificar a los candidatos por una nueva propuesta'),
    'CAN_CANDIDATES_NOT_COMMIT': (False, 'Pueden los candidatos NO comprometerse?'),
    'NO_REPLY_MAIL': ("no-reply@localhost", 'Cuenta email de envio de correos'),
    'EMAIL_LOCALPART': ("municipales2016", 'Cuenta email localhost'),
    'EMAIL_DOMAIN': ("votainteligente.cl", 'Nombre dominio'),
    'MAX_AMOUNT_OF_MAILS_TO_CANDIDATE': (3, 'Numero maximo de envios de emails a candidatos'),
    'TWITTER_TOKEN': ('', 'Twitter token'),
    'MAILCHIMP_U': ('perrito', 'MAILCHIMP u la partecita u del mailchimp'),
    'MAILCHIMP_ID': ('gatito', 'MAILCHIMP u la partecita u del mailchimp'),
    'MARKED_AREAS': ("", u'Areas que tienen alguna marca'),
    'CANDIDATE_ABSOLUTE_URL_USING_AREA': (True, u'para ver el perfil de los candidatos utilziamos el territorio o utilizamos la elección a la que pertenece?'),
    'TWITTER_TOKEN_KEY': ('', 'Twitter token key'),
    'MENU_CIUDADANO_EN_DROPDOWN': (False, u'El menú ciudadano va en el dropdown menu que está arriba en la derecha?'),
    'TWITTER_CON_KEY': ('', 'Twitter connection key'),
    'TWITTER_CON_SECRET_KEY': ('', 'Twitter connection secret key'),
    'HIDDEN_AREAS': ('', 'Seccion oculta'),
    'DEFAULT_ELECTION_ID': (1, u'La elección que aparece en /candidaturas'),
    'NAV_BAR': ('profiles, questionary, soulmate, facetoface, ask, ranking', 'Menu de navegacion'),
    'SHOW_RIBBON_IN_CANDIDATE': (False, u"Debería aparecerles la franja roja que dice 'No se ha compormetido?'"),
    'SHOW_ALL_CANDIDATES_IN_THIS_ORDER': ("", u"Mostrar todos los candidatos en la parte de /candidatos? "),
    'CAN_CREATE_TEST_PROPOSAL': (False, u'Se pueden crear propuestas de prueba?'),
    'SEARCH_SUBSCRIPTION_ENABLED': (True, u'Suscribirse a una búsqueda está habilitado? esto sólo esconde los links.'),
    'WEBSITE_METADATA_AUTHOR': ('', 'Nombre del autor'),
    'PERIODIC_REPORTS_ENABLED': (False, u'Están habilitadas los envíos de reportes periódicos sobre las propuestas?'),
    'WEBSITE_METADATA_DESCRIPTION': ('', 'Descripcion del sitio'),
    'WEBSITE_METADATA_KEYWORD': ('', 'Palabras claves del sitio'),
    'WEBSITE_OGP_TITLE': ('VotaInteligente', 'Titulo OpenGraph Protocol'),
    'WEBSITE_OGP_TYPE': ('website', 'Tipo OpenGraph Protocol'),
    'WEBSITE_OGP_URL': ('https://www.mi-domain.org/', 'URL base OpenGraph Protocol'),
    'WEBSITE_OGP_DESCRIPTION': ('', 'Descripción del sitio para OpenGraph Protocol'),
    'WEBSITE_OGP_APP_ID': ('APPID', 'Facebokk App ID'),
    'WEBSITE_DISQUS_ENABLED': (True, 'Activar Disqus'),
    'WEBSITE_DISQUS_SHORTNAME': (True, 'Disqus shortname'),
    'WEBSITE_DISQUS_DEV_MODE': (False, 'Modo desarrollo'),
    'WEBSITE_GA_CODE': ('UA-XXXXX-X', 'Codigo Google Analytics'),
    'WEBSITE_GA_NAME': ('votainteligente.cl', 'Nombre Google Analytics'),
    'WEBSITE_GA_GSITE_VERIFICATION': ('BCyMskdezWX8ObDCMsm_1zIQAayxYzEGbLve8MJmxHk', 'Verificacion Google Site'),
    'WEBSITE_IMGUR_CLIENT_ID': ('eb18642b5b220484864483b8e21386c3', 'Imgur'),
    'WEBSITE_GENERAL_SETTINGS_HOME_TITLE': ('Lorem ipsum dolor sit amet, consectetur adipisicing elit.', 'Titulo Home'),
    'WEBSITE_TWITTER_HASHTAG': ('votainteligente', 'Twitter Hashtags'),
    'WEBSITE_TWITTER_TEXT': ('Conoce a tus candidat@s y encuentra a tu Media Naranja Política en', 'Texto twitts'),
    'AYUDANOS_TEXTO1' : (u'Tenemos poca info de candidatos. Ayuda a candidatos y electores haciendo que respondan la ½ naranja', 'texto 1 del ayudanos'),
    'AYUDANOS_TEXTO2' : (u'Si no conoces a tus candidatos y no sabes ', 'texto 2 del ayudanos'),
    'AYUDANOS_TEXTO3' : (u'Invita a tus candidatos a dejar su información en VotaInteligente.cl para saber qué piensan y ', 'texto 3 del ayudanos'),
    'AYUDANOS_TEXTO4' : (u'Necesitamos que los candidatos compartan su infromación con los vecinos, para conocerlos y saber ', 'texto 4 del ayudanos'),
    'AYUDANOS_ORGANIZACIONES' : (u'Ya puedes comprometerte con nuestras propuestas ', 'texto ayudanos en las organizaciones'),
    "CANDIDATE_SEARCH_ENABLED": (True, 'La busqueda de candidatos está habilitada???'),
    'AYUDANOS_TEXTO_CANDIDATOS' : (u'Ya puedes comprometerte con nuestras propuestas ', 'texto a los candidatos del ayudanos'),
    'AYUDANOS_PROPUESTA': (u'Ya puedes comprometerte en votainteligente.cl', 'texto a los candidatos del ayudanos específico de cada propuesta'),
    'MOSTRAR_AYUDANOS_PROPUESTA': (False, 'texto a los candidatos del ayudanos específico de cada propuesta'),
    'DEFAULT_12_N_QUESTIONS_IMPORTANCE': (0.5, "Importancia de las preguntas en la media naranja"),
    'DEFAULT_12_N_PROPOSALS_IMPORTANCE': (0.5, "Importancia de las propuestas en la media naranja"),
    'SHOW_MAIL_NOT_TEMPLATE': (True, 'mostrar el mail que se envía en lugar de un html'),
    'N_CANDIDATOS_RESULTADO_12_N': (3, u'Máximo número de candidatos en el resultado de la 1/2 Naranja'),
    'MEDIA_NARANJA_MAX_NUM_PR': (20, u'Máximo número de propuestas listadas en la 1/2 Naranja'),
    'MEDIA_NARANJA_MAX_SELECT_PROPOSALS': (5, u'Máximo número de propuestas seleccionables en la 1/2 Naranja'),
    'PRUEBAS_DE_CARGA_MEDIA_NARANJA': (False, u'Esto baja el csrf para las pruebas de la medianaranja2'),
    'MEDIA_NARANJA_QUESTIONS_ENABLED': (True, u'Si bajas esto la 1/2 n sólo usará propuestas ciudadanas'),

    'ESTRATEGIA_SELECCION_PROPUESTAS': ("getter", u'Qué estrategia usamos para mostrar propuestas en la 1/2 naranja', 'proposals_getter_for_12_n'),
    'DONT_SHOW_AREAS_IN_PROPOSAL_WIZARD': (True, u'No muestres las areas en el wizard de creación de propuestas'),
}