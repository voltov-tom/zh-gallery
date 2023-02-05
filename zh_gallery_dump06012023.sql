--
-- PostgreSQL database dump
--

-- Dumped from database version 12.12 (Ubuntu 12.12-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.12 (Ubuntu 12.12-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.account_emailaddress OWNER TO voltov;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.account_emailaddress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailaddress_id_seq OWNER TO voltov;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.account_emailaddress_id_seq OWNED BY public.account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE public.account_emailconfirmation OWNER TO voltov;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.account_emailconfirmation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailconfirmation_id_seq OWNER TO voltov;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.account_emailconfirmation_id_seq OWNED BY public.account_emailconfirmation.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO voltov;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO voltov;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO voltov;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO voltov;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO voltov;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO voltov;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO voltov;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO voltov;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO voltov;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO voltov;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO voltov;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO voltov;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: core_about; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.core_about (
    id bigint NOT NULL,
    body text,
    image character varying(100),
    body_en text,
    body_ru text
);


ALTER TABLE public.core_about OWNER TO voltov;

--
-- Name: core_about_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.core_about_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_about_id_seq OWNER TO voltov;

--
-- Name: core_about_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.core_about_id_seq OWNED BY public.core_about.id;


--
-- Name: core_maincategory; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.core_maincategory (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    title_en character varying(255),
    title_ru character varying(255)
);


ALTER TABLE public.core_maincategory OWNER TO voltov;

--
-- Name: core_maincategory_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.core_maincategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_maincategory_id_seq OWNER TO voltov;

--
-- Name: core_maincategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.core_maincategory_id_seq OWNED BY public.core_maincategory.id;


--
-- Name: core_mediaitem; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.core_mediaitem (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying(255),
    image character varying(100) NOT NULL,
    subcategory_id bigint,
    views integer NOT NULL,
    like_time timestamp with time zone NOT NULL,
    description_en character varying(255),
    description_ru character varying(255),
    title_en character varying(255),
    title_ru character varying(255)
);


ALTER TABLE public.core_mediaitem OWNER TO voltov;

--
-- Name: core_mediaitem_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.core_mediaitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_mediaitem_id_seq OWNER TO voltov;

--
-- Name: core_mediaitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.core_mediaitem_id_seq OWNED BY public.core_mediaitem.id;


--
-- Name: core_mediaitem_likes; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.core_mediaitem_likes (
    id bigint NOT NULL,
    mediaitem_id bigint NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.core_mediaitem_likes OWNER TO voltov;

--
-- Name: core_mediaitem_likes_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.core_mediaitem_likes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_mediaitem_likes_id_seq OWNER TO voltov;

--
-- Name: core_mediaitem_likes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.core_mediaitem_likes_id_seq OWNED BY public.core_mediaitem_likes.id;


--
-- Name: core_mediaitemreview; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.core_mediaitemreview (
    id bigint NOT NULL,
    content text,
    date_added timestamp with time zone NOT NULL,
    media_item_id bigint NOT NULL,
    user_id integer NOT NULL,
    edited boolean NOT NULL
);


ALTER TABLE public.core_mediaitemreview OWNER TO voltov;

--
-- Name: core_mediaitemreview_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.core_mediaitemreview_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_mediaitemreview_id_seq OWNER TO voltov;

--
-- Name: core_mediaitemreview_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.core_mediaitemreview_id_seq OWNED BY public.core_mediaitemreview.id;


--
-- Name: core_subcategory; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.core_subcategory (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    category_id bigint,
    image character varying(100),
    description character varying(255),
    description_en character varying(255),
    description_ru character varying(255),
    title_en character varying(255),
    title_ru character varying(255)
);


ALTER TABLE public.core_subcategory OWNER TO voltov;

--
-- Name: core_subcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.core_subcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_subcategory_id_seq OWNER TO voltov;

--
-- Name: core_subcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.core_subcategory_id_seq OWNED BY public.core_subcategory.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO voltov;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO voltov;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO voltov;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO voltov;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO voltov;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO voltov;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO voltov;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO voltov;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO voltov;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data text NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialaccount OWNER TO voltov;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.socialaccount_socialaccount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialaccount_id_seq OWNER TO voltov;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.socialaccount_socialaccount_id_seq OWNED BY public.socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL
);


ALTER TABLE public.socialaccount_socialapp OWNER TO voltov;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.socialaccount_socialapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialapp_id_seq OWNER TO voltov;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.socialaccount_socialapp_id_seq OWNED BY public.socialaccount_socialapp.id;


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.socialaccount_socialapp_sites (
    id bigint NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialapp_sites OWNER TO voltov;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.socialaccount_socialapp_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialapp_sites_id_seq OWNER TO voltov;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.socialaccount_socialapp_sites_id_seq OWNED BY public.socialaccount_socialapp_sites.id;


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: voltov
--

CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialtoken OWNER TO voltov;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: voltov
--

CREATE SEQUENCE public.socialaccount_socialtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialtoken_id_seq OWNER TO voltov;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: voltov
--

ALTER SEQUENCE public.socialaccount_socialtoken_id_seq OWNED BY public.socialaccount_socialtoken.id;


--
-- Name: account_emailaddress id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailaddress ALTER COLUMN id SET DEFAULT nextval('public.account_emailaddress_id_seq'::regclass);


--
-- Name: account_emailconfirmation id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('public.account_emailconfirmation_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: core_about id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_about ALTER COLUMN id SET DEFAULT nextval('public.core_about_id_seq'::regclass);


--
-- Name: core_maincategory id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_maincategory ALTER COLUMN id SET DEFAULT nextval('public.core_maincategory_id_seq'::regclass);


--
-- Name: core_mediaitem id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem ALTER COLUMN id SET DEFAULT nextval('public.core_mediaitem_id_seq'::regclass);


--
-- Name: core_mediaitem_likes id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem_likes ALTER COLUMN id SET DEFAULT nextval('public.core_mediaitem_likes_id_seq'::regclass);


--
-- Name: core_mediaitemreview id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitemreview ALTER COLUMN id SET DEFAULT nextval('public.core_mediaitemreview_id_seq'::regclass);


--
-- Name: core_subcategory id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_subcategory ALTER COLUMN id SET DEFAULT nextval('public.core_subcategory_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: socialaccount_socialaccount id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: socialaccount_socialapp id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_id_seq'::regclass);


--
-- Name: socialaccount_socialapp_sites id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_sites_id_seq'::regclass);


--
-- Name: socialaccount_socialtoken id; Type: DEFAULT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialtoken_id_seq'::regclass);


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
3	zhenya@zh-gallery.ru	t	t	2
5	voltovtom92@gmail.com	t	t	6
6	voltov-tom@mail.ru	t	t	7
7	bletmetest@gmail.com	f	t	8
8	voltoff69@yandex.ru	t	t	9
9	bletmetest@yandex.ru	t	t	10
10	admin@msglaz.ru	f	t	11
11	zh-gallery.ru@yandex.ru	f	t	12
12	zh-gallery@yandex.ru	t	t	13
13	merenkovamaria0802@yandex.ru	t	t	14
14	test1996lena@yandex.ru	t	t	15
15	ghpvebem@vdnh.online	f	t	16
16	kat-servise56@yandex.ru	f	t	17
17	creawert@rambler.ru	f	t	18
18	cazackovkim@yandex.ru	f	t	19
19	azat-fattakhov@inbox.ru	f	t	20
20	ahmarlapin@yandex.ru	f	t	21
\.


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add main category	7	add_maincategory
26	Can change main category	7	change_maincategory
27	Can delete main category	7	delete_maincategory
28	Can view main category	7	view_maincategory
29	Can add sub category	8	add_subcategory
30	Can change sub category	8	change_subcategory
31	Can delete sub category	8	delete_subcategory
32	Can view sub category	8	view_subcategory
33	Can add media item	9	add_mediaitem
34	Can change media item	9	change_mediaitem
35	Can delete media item	9	delete_mediaitem
36	Can view media item	9	view_mediaitem
37	Can add site	10	add_site
38	Can change site	10	change_site
39	Can delete site	10	delete_site
40	Can view site	10	view_site
41	Can add email address	11	add_emailaddress
42	Can change email address	11	change_emailaddress
43	Can delete email address	11	delete_emailaddress
44	Can view email address	11	view_emailaddress
45	Can add email confirmation	12	add_emailconfirmation
46	Can change email confirmation	12	change_emailconfirmation
47	Can delete email confirmation	12	delete_emailconfirmation
48	Can view email confirmation	12	view_emailconfirmation
49	Can add social account	13	add_socialaccount
50	Can change social account	13	change_socialaccount
51	Can delete social account	13	delete_socialaccount
52	Can view social account	13	view_socialaccount
53	Can add social application	14	add_socialapp
54	Can change social application	14	change_socialapp
55	Can delete social application	14	delete_socialapp
56	Can view social application	14	view_socialapp
57	Can add social application token	15	add_socialtoken
58	Can change social application token	15	change_socialtoken
59	Can delete social application token	15	delete_socialtoken
60	Can view social application token	15	view_socialtoken
61	Can add media item review	16	add_mediaitemreview
62	Can change media item review	16	change_mediaitemreview
63	Can delete media item review	16	delete_mediaitemreview
64	Can view media item review	16	view_mediaitemreview
65	Can add about	17	add_about
66	Can change about	17	change_about
67	Can delete about	17	delete_about
68	Can view about	17	view_about
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
6	!aC3HI59HJIz9CV4XBdRkzlHMInfnmXIAo6luiVEJ	2022-07-20 10:29:28.85971+00	f	timofei	Timofei	Voltov	voltovtom92@gmail.com	f	t	2022-01-28 21:25:06.707203+00
10	pbkdf2_sha256$320000$w8njpj3jBE94B2UWbi6RZX$buORyv/XcvPbfzm6q0YJecAHcoqIVAN1GuXgtRY9W7s=	\N	f	Letmetest			bletmetest@yandex.ru	f	t	2022-04-22 12:22:11.867943+00
8	pbkdf2_sha256$320000$cBMAOltYE1c3pSCcY05NWA$XTRU3ZAxNKuR9h2e0nYW6a7Y8/L3o0UrqS0zuQRuXaU=	\N	f	Test			bletmetest@gmail.com	f	t	2022-04-20 11:31:42.036229+00
11	pbkdf2_sha256$320000$Qe3WQvMnCVLzJwdedJaymU$vQYJXVnYy3sIYZcLoxCKuuzTBzqBzGegBwZfd4lndJU=	\N	f	admin			admin@msglaz.ru	f	t	2022-04-23 03:12:45.430328+00
12	pbkdf2_sha256$320000$85etUfMO6RoRudgR9drI8s$R5tDtV2XwB/0cg0CYkWUGwKb6IxpAiHaboHskhGe66M=	\N	f	zh-gallery.ru			zh-gallery.ru@yandex.ru	f	t	2022-04-23 08:47:39.710745+00
14	pbkdf2_sha256$320000$kzRaXIO8snfbtMFlHbXE95$0wGOkf4RD+3fcrsle167+imLfHYr8R+CuO4Duo8Trsg=	2022-04-26 11:54:35.806103+00	f	merenkovamaria0802			merenkovamaria0802@yandex.ru	f	t	2022-04-26 11:53:27.769024+00
17	pbkdf2_sha256$320000$THq5wTyKqB0eJaUPuSTE6q$jO2x9OcVQvD66KMgPox6gQdTTb+9K/Ktfr9rXf0apJw=	\N	f	DanielNub			kat-servise56@yandex.ru	f	t	2022-11-08 22:41:43.177002+00
18	pbkdf2_sha256$320000$eGvtcsYX09FdnGSAjygQcj$rCs++jIZqfJHgESq1gZUGk8fqmPQncfOKUAu4+uSv9U=	\N	f	Jeffreyfrede			creawert@rambler.ru	f	t	2022-11-17 06:47:26.774974+00
19	pbkdf2_sha256$320000$e0QfoHXtWyN1yLW0VX222b$k5YL7WCwb/iS8vP9FcdmGpFGGra+SyXx8vsz/IHl7Dk=	\N	f	Svetlanaanewedomose			cazackovkim@yandex.ru	f	t	2022-11-19 02:51:10.499628+00
7	pbkdf2_sha256$320000$GqHQaSzqT62Zwr4b5Ds62O$oQNDimHqLIlwM/vxvLnTsDAxnyHBEBaErYyQaAvCNg8=	2022-04-30 05:58:32.614803+00	f	voltov-tom			voltov-tom@mail.ru	f	t	2022-01-28 21:30:02.466806+00
9	pbkdf2_sha256$320000$C3CaTjueVUm3adauPtQK7F$zvKoOsemZZc52N4Fdovdus/ibSVtW7yw/5ExYT3T1wE=	2022-11-23 12:29:12.519716+00	f	voltoff			voltoff69@yandex.ru	f	t	2022-04-20 15:02:59.674349+00
2	pbkdf2_sha256$320000$NZgrGHsnhJhMInJzaoNLlU$XNU/iQzAKmZhfF09JmuYlHGzDu6AbfmScQmMc4YFmVg=	2022-11-26 21:15:20.877105+00	t	zhenya			zhenya@zh-gallery.ru	t	t	2021-12-31 00:03:30+00
20	pbkdf2_sha256$320000$W58j6TFwFx0VQvdEagDzEg$IUIkRPjWLtRhhFfUPqEm4SGh74U3KMr3goZBsNnKE3c=	\N	f	Азат			azat-fattakhov@inbox.ru	f	t	2022-12-06 01:04:52.860854+00
21	pbkdf2_sha256$320000$OsAF3u37CvvnwjQGcAy4ht$jM7/kOCs3jFOXFsiktwb+3jogLIN/qx6mqj1PSYDlAE=	\N	f	IrinaIndidence			ahmarlapin@yandex.ru	f	t	2022-12-23 13:14:42.718658+00
15	pbkdf2_sha256$320000$x2LL3CMswmmQdGIV7wwCBk$h/d0wcDA5jL6xctxl4YVdbt8NU1MCi0jCIs1h1KfjIE=	2022-05-16 07:42:49.231707+00	f	Test123			test1996lena@yandex.ru	f	t	2022-05-16 07:41:31.699346+00
13	pbkdf2_sha256$320000$K6joSVUL9XKlHgZMkCzfCR$pBfbii3Aqq73i+oDm33sorxLsqW1ci+Ud5QOBGFIBkU=	2022-05-16 07:45:33.244557+00	f	zh-gallery			zh-gallery@yandex.ru	f	t	2022-04-23 08:50:39.578984+00
16	pbkdf2_sha256$320000$FC3CDSErhnSdsjv20igoLP$76UJxT6m0pEA5J01G08CKXlM88QmhoJNm0ezKIn8elo=	\N	f	Dzxetgob			ghpvebem@vdnh.online	f	t	2022-05-20 06:08:57.529828+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: core_about; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.core_about (id, body, image, body_en, body_ru) FROM stdin;
1	Привет и добро пожаловать в мою галерею! Меня зовут Евгения, но можно просто Женя, отсюда и появилось сокращение ZH в наименовании… Обычно я снимаю на плёнку и рисую иллюстрации для себя, просто потому что мне это нравится…но кроме этого я занимаюсь изготовлением скетчбуков, ежедневников , фотоальбомов и других различных канцелярских товаров на продажу, которые можно увидеть в моём Инстаграм аккаунте. А в этой галерее я бы хотела заполнить всё розовым…на самом деле не только розовым, хоть это и правда мой любимый цвет! Я буду, правда, очень благодарна вашему вниманию и поддержке!	2C616B84-40FC-4829-A16A-F37B062EF3DF.jpeg	Hello and welcome to my gallery! My name is Evgeniya or a simple Zhenya, so that’s why ZH in the title… Usually I take a film photos and a digital illustrations for myself, just because I like it…but also I create a sketchbooks a planners a photo albums and the other stationary staff for sale , whose you can see at my instagram. In this gallery I would like prefer to you my crazy pink visuals… actually not only these but it’s really my favourite colour! I’m really appreciate for your attention and support !	Привет и добро пожаловать в мою галерею! Меня зовут Евгения, но можно просто Женя, отсюда и появилось сокращение ZH в наименовании… Обычно я снимаю на плёнку и рисую иллюстрации для себя, просто потому что мне это нравится…но кроме этого я занимаюсь изготовлением скетчбуков, ежедневников , фотоальбомов и других различных канцелярских товаров на продажу, которые можно увидеть в моём Инстаграм аккаунте. А в этой галерее я бы хотела заполнить всё розовым…на самом деле не только розовым, хоть это и правда мой любимый цвет! Я буду, правда, очень благодарна вашему вниманию и поддержке!
\.


--
-- Data for Name: core_maincategory; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.core_maincategory (id, title, slug, title_en, title_ru) FROM stdin;
1	GALLERIES	galleries	GALLERIES	ГАЛЕРЕИ
2	IN THE INTERIOR	in-the-interior	IN THE INTERIOR	В ИНТЕРЬЕРЕ
\.


--
-- Data for Name: core_mediaitem; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.core_mediaitem (id, title, slug, description, image, subcategory_id, views, like_time, description_en, description_ru, title_en, title_ru) FROM stdin;
12	Hey girl	hey-girl	Милашка	2FC80D87-6BB7-4B33-A7B6-A4DB2BC26CD1.jpeg	1	139	2023-01-02 07:37:06.123249+00	Cutie	Милашка	Hey girl	Hey girl
19	Mark	mark	Child	997F3BD0-F323-4BDB-97E3-EC9F7EC91CED.jpeg	2	322	2023-01-04 15:52:55.253932+00	Child	Child	Mark	Mark
20	DojaCat	dojacat	SaySo	BD7ED998-58F7-4F35-9068-ECFEE1F78A32.jpeg	2	159	2023-01-04 16:06:24.181522+00	SaySo	SaySo	DojaCat	DojaCat
18	Flowers	flowers	Половинка сердца	98E86A3D-0C2F-49F5-8675-1A1A24ABAEA7.jpeg	2	166	2023-01-05 22:48:42.298656+00	Part of the heart	Половинка сердца	Flowers	Flowers
6	Witches	witches	My friends is a best photomodels	5A0B631F-1175-442A-A654-77EA67AB0B37.jpeg	1	102	2023-01-01 08:01:17.78795+00	My friends is a best photomodels	Мои подруги-мои лучшие модели	Witches	Witches
13	In the corner	in-the-corner	This is me in the Gallery	E29AD2F5-6632-4E22-BA64-97383290CF43.jpeg	1	101	2023-01-01 08:01:22.633074+00	This is me in the Gallery	Это я в картинной галерее	In the corner	In the corner
25	“Y” keychain	y-keychain	Эпоксидная смола	4C21C6E6-BD53-4977-8D61-F43CCD0CC290.jpeg	3	270	2023-01-01 22:36:01.46922+00	Epoxy resin	Эпоксидная смола	“Y” keychain	“Y” keychain
23	Suga	suga	Скетчбук и брелок	0C6931CA-EC28-4A3E-B9A7-CACC8E269C96.jpeg	3	110	2023-01-02 05:18:33.835552+00	Sketchbook and keychain	Скетчбук и брелок	Suga	Suga
17	VHS	vhs	Кассета и старый снимок	7FDBA194-9521-411C-B842-626EA1C339A3.jpeg	2	116	2023-01-06 00:38:35.254219+00	VHS cassette and retro photo	Кассета и старый снимок	VHS	VHS
21	NingNing	ningning	Aespa	49BB43C2-3E32-4ADB-AC6E-E582FBF48963.jpeg	2	91	2022-12-09 04:07:34.109655+00	Aespa	Aespa	NingNing	NingNing
15	Party time	party-time	Молоды и свободны	0E94492E-4BDD-4FC3-8F0C-B2B5AABF6422.jpeg	2	145	2023-01-02 06:33:24.966031+00	young and free	Молоды и свободны	Party time	Party time
5	In  black 4	in-black-4	Нежный ангел в чёрном	BB04605A-DD3B-44C1-8925-5492E217B6AC.jpeg	1	86	2023-01-06 06:25:09.861904+00	Soft angel in black	Нежный ангел в чёрном	In  black 4	In  black 4
3	In black  2	in-black-2	Строгий взгляд	686A889C-E70F-43A4-8A7A-DBD774A206CB.jpeg	1	76	2023-01-03 01:35:18.302466+00	Strict eyes	Строгий взгляд	In black  2	In black  2
22	AvuChan	avuchan	QueenBee	D1BDC4BB-51FA-478B-AC28-6C1149727C12.jpeg	2	121	2023-01-03 11:43:01.977183+00	QueenBee	QueenBee	AvuChan	AvuChan
16	Lisa	lisa	ЛаЛиса Манобан	F864326E-2C11-4C6B-A504-25B2069CC94D.jpeg	2	78	2022-12-08 13:19:53.627288+00	LaLisa Manoban	ЛаЛиса Манобан	Lisa	Lisa
10	In black	in-black	На фоне розовой стены	8CEE188A-7248-4966-9715-5ED68EEAFB43.jpeg	1	129	2023-01-04 00:01:28.134757+00	Pink wall	На фоне розовой стены	In black	In black
4	Rain	rain	Красивый серый дождь	9AEB0284-F36A-4061-BB41-A55AA727AF22.jpeg	1	97	2023-01-04 07:31:43.763509+00	The grey beautiful rain	Красивый серый дождь	Rain	Rain
8	In the tree’s shadow	in-the-trees-shadow	Солнечная девочка	6819C955-94FA-4E08-8451-9EE4706559F4.jpeg	1	90	2022-12-29 18:41:24.918784+00	Sunny girl	Солнечная девочка	In the tree’s shadow	In the tree’s shadow
9	In black 3	in-black-3	Сахарная вата	F70B6E0C-AB38-4C89-8F5F-0396B5DEB837.jpeg	1	103	2023-01-05 02:16:12.965423+00	Cotton candy	Сахарная вата	In black 3	In black 3
7	Supernatural	supernatural	Small black dress	F61641C2-414C-40C6-88A2-90DA28862167.jpeg	1	84	2023-01-01 08:01:31.755874+00	Small black dress	Маленькое чёрное платье	Supernatural	Supernatural
1	Sun chilling	sun-chilling	Солнечный портрет	F4831A09-9407-48AD-ABAD-1DEBBCDDB65C.jpeg	1	95	2023-01-05 11:11:06.266589+00	Sunlight portrait	Солнечный портрет	Sun chilling	Sun chilling
11	Sky	sky	Богиня гор	33841CB3-260A-4825-AAE9-2870137BA282.jpeg	1	98	2022-12-30 06:09:32.792054+00	God of the mountains	Богиня гор	Sky	Sky
24	Holographic cover	holographic-cover	Голографическая-обложка	D2E9883A-6D8A-48CC-BA49-FF80BEC9FEE7.jpeg	3	128	2023-01-05 11:39:48.384202+00	With BTS	Голографическая-обложка	Holographic cover	Holographic cover
2	Rock	rock	Богиня леса	DEA9AAFC-2CAD-4FED-A56E-D5CAD952F621.jpeg	1	61	2023-01-05 14:20:57.131113+00	God of the forest	Богиня леса	Rock	Rock
\.


--
-- Data for Name: core_mediaitem_likes; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.core_mediaitem_likes (id, mediaitem_id, user_id) FROM stdin;
19	17	2
21	10	2
22	1	2
23	10	6
25	6	6
26	18	6
27	5	6
28	5	7
29	10	7
30	6	7
31	20	6
34	20	7
35	22	7
36	23	2
37	25	2
38	24	2
40	23	7
41	24	7
42	15	7
43	18	7
44	16	7
46	9	7
47	25	6
48	19	7
49	17	7
50	16	6
51	15	6
53	3	6
54	21	2
56	20	2
58	18	2
59	19	6
60	25	7
61	3	7
62	19	15
63	11	15
64	8	13
65	2	13
66	19	2
67	24	6
68	23	6
69	17	6
72	3	2
73	15	2
74	23	9
75	4	2
\.


--
-- Data for Name: core_mediaitemreview; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.core_mediaitemreview (id, content, date_added, media_item_id, user_id, edited) FROM stdin;
3	So nice	2022-01-31 16:17:40.995735+00	20	6	f
5	Like it!	2022-02-06 09:50:23.282282+00	25	6	t
8	Круто!	2022-04-04 07:43:32.332358+00	19	2	f
1	Мне нравится масштаб, видно объем.	2022-01-28 21:28:44.953129+00	18	6	t
11	очень хорошо	2022-07-20 15:57:42.663128+00	15	6	f
13	замечательно	2022-11-21 05:45:08.262911+00	25	9	t
12	прекрасно	2022-11-21 05:40:58.955563+00	19	9	t
15	Bank 	2022-11-23 12:29:25.703864+00	23	9	f
\.


--
-- Data for Name: core_subcategory; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.core_subcategory (id, title, slug, category_id, image, description, description_en, description_ru, title_en, title_ru) FROM stdin;
2	Графика	grafika	1	2DDD439D-3669-41F3-80CD-E452E658EB34.jpeg	Графика	Digital graphics	Графика	Graphics	Графика
1	Фотопленка	fotoplenka	1	404BDDFD-316C-422D-9256-11F370F08FFF.jpeg	Пленочные фото	FilmPhotography	Пленочные фото	FilmPhotography	Фотопленка
3	Блокноты	bloknoty	1	9BE7E73F-D547-424F-B919-2AF667F03B78.jpeg	Блокноты ручной работы	Sketchbooks, keychains, photo albums	Блокноты ручной работы	Notebooks	Блокноты
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2021-12-31 00:05:55.698663+00	1	root	3		4	2
2	2021-12-31 21:24:35.936443+00	1	FilmPHOTO	1	[{"added": {}}]	7	2
3	2021-12-31 21:26:23.07443+00	1	Galleries	2	[{"changed": {"fields": ["Title"]}}]	7	2
4	2021-12-31 21:33:48.647501+00	1	FilmPhotography	1	[{"added": {}}]	8	2
5	2021-12-31 21:51:51.050977+00	1	FilmPhotography	2	[]	8	2
6	2022-01-01 08:31:58.679497+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
7	2022-01-01 08:32:07.430791+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
8	2022-01-01 11:57:21.324095+00	1	Sun chilling	1	[{"added": {}}]	9	2
9	2022-01-01 11:58:21.170631+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
10	2022-01-01 11:59:29.631355+00	1	Sun chilling	2	[{"changed": {"fields": ["Image"]}}]	9	2
11	2022-01-01 12:00:19.360573+00	2	Rock	1	[{"added": {}}]	9	2
12	2022-01-01 12:00:56.264818+00	3	K-pop	1	[{"added": {}}]	9	2
13	2022-01-01 12:01:33.594669+00	4	Metall	1	[{"added": {}}]	9	2
14	2022-01-01 12:01:59.104165+00	5	Baby	1	[{"added": {}}]	9	2
15	2022-01-01 12:02:44.184281+00	6	Meat	1	[{"added": {}}]	9	2
16	2022-01-01 13:14:16.214747+00	5	Baby black	2	[{"changed": {"fields": ["Title", "Description", "Image"]}}]	9	2
17	2022-01-01 13:23:23.518491+00	3	Baby black	2	[{"changed": {"fields": ["Title", "Description", "Image"]}}]	9	2
18	2022-01-01 14:30:04.843918+00	3	Pink wall	2	[{"changed": {"fields": ["Title"]}}]	9	2
19	2022-01-01 14:34:36.840779+00	6	Witches	2	[{"changed": {"fields": ["Title", "Description", "Image"]}}]	9	2
20	2022-01-01 14:51:23.817633+00	4	Rain	2	[{"changed": {"fields": ["Title", "Description", "Image"]}}]	9	2
21	2022-01-01 14:54:12.625446+00	2	Rock	2	[{"changed": {"fields": ["Description", "Image"]}}]	9	2
22	2022-01-01 14:57:20.371963+00	1	Sun chilling	2	[{"changed": {"fields": ["Description", "Image"]}}]	9	2
23	2022-01-01 15:08:57.239625+00	7	Supernatural	1	[{"added": {}}]	9	2
24	2022-01-01 15:35:49.795597+00	8	In the tree’s shadow	1	[{"added": {}}]	9	2
25	2022-01-01 15:42:53.642743+00	9	Baby black 3	1	[{"added": {}}]	9	2
26	2022-01-01 15:43:14.287809+00	3	Baby pink 2	2	[{"changed": {"fields": ["Title"]}}]	9	2
27	2022-01-01 15:43:59.559834+00	10	Baby black	1	[{"added": {}}]	9	2
28	2022-01-01 15:55:02.542623+00	11	Rock	1	[{"added": {}}]	9	2
29	2022-01-01 15:55:21.094989+00	3	Baby black  2	2	[{"changed": {"fields": ["Title"]}}]	9	2
30	2022-01-01 15:55:31.689891+00	5	Baby black 4	2	[{"changed": {"fields": ["Title"]}}]	9	2
31	2022-01-01 16:01:02.510615+00	12	Hey girl	1	[{"added": {}}]	9	2
32	2022-01-01 16:07:38.801599+00	13	In the corner	1	[{"added": {}}]	9	2
33	2022-01-02 19:19:50.564981+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
34	2022-01-02 19:28:05.085298+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
35	2022-01-02 19:28:25.216841+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
36	2022-01-02 19:31:28.050239+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
37	2022-01-02 19:31:42.323015+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
38	2022-01-02 19:32:56.115013+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
39	2022-01-02 19:33:49.26839+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
40	2022-01-02 19:35:30.192279+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
41	2022-01-02 19:35:37.135752+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
42	2022-01-02 19:48:26.029659+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
43	2022-01-02 19:48:32.383414+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
44	2022-01-02 20:06:32.00718+00	14	1221	1	[{"added": {}}]	9	2
45	2022-01-02 20:06:54.48508+00	14	1221	3		9	2
46	2022-01-05 15:26:21.356444+00	1	FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
47	2022-01-05 20:42:59.031621+00	8	In the tree’s shadow	2	[]	9	2
48	2022-01-05 20:44:08.17645+00	8	In the tree’s shadow	2	[]	9	2
49	2022-01-08 06:45:00.508196+00	1	GALLERIES	2	[{"changed": {"fields": ["Title"]}}]	7	2
50	2022-01-08 06:46:01.415421+00	2	GRAPHICS	1	[{"added": {}}]	7	2
51	2022-01-08 06:47:21.582799+00	2	IN INTERIOR	2	[{"changed": {"fields": ["Title"]}}]	7	2
52	2022-01-08 06:49:11.38427+00	2	GALLERIES: GRAPHICS	1	[{"added": {}}]	8	2
53	2022-01-08 07:09:42.663536+00	15	GALLERIES: GRAPHICS: Dance girl	1	[{"added": {}}]	9	2
54	2022-01-08 07:11:30.543891+00	16	GALLERIES: GRAPHICS: Lisa	1	[{"added": {}}]	9	2
55	2022-01-08 07:18:16.126232+00	17	GALLERIES: GRAPHICS: VHS	1	[{"added": {}}]	9	2
56	2022-01-08 07:20:18.351307+00	18	GALLERIES: GRAPHICS: Flowers	1	[{"added": {}}]	9	2
57	2022-01-08 10:11:03.834354+00	2	GALLERIES: GRAPHICS	2	[{"changed": {"fields": ["Image"]}}]	8	2
58	2022-01-08 10:12:42.72499+00	1	GALLERIES: FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
59	2022-01-10 18:13:04.945979+00	1	zh-gallery.ru	2	[{"changed": {"fields": ["Domain name", "Display name"]}}]	10	2
60	2022-01-10 18:14:42.097827+00	1	zh-gallery	1	[{"added": {}}]	14	2
61	2022-01-21 10:38:27.965408+00	1	GALLERIES: FilmPhotography	2	[{"changed": {"fields": ["Image"]}}]	8	2
62	2022-01-21 10:57:08.79683+00	11	11, GALLERIES: FilmPhotography: Sky	2	[{"changed": {"fields": ["Title", "Likes"]}}]	9	2
63	2022-01-21 10:58:13.790103+00	11	11, GALLERIES: FilmPhotography: Sky	2	[{"changed": {"fields": ["Likes"]}}]	9	2
64	2022-01-21 12:10:36.417141+00	1	About object (1)	1	[{"added": {}}]	17	2
65	2022-01-21 18:05:41.231499+00	1	About object (1)	2	[{"changed": {"fields": ["Image"]}}]	17	2
66	2022-01-27 14:42:01.619574+00	2	zhenya	2	[{"changed": {"fields": ["Email address"]}}]	4	2
67	2022-01-27 14:42:14.556199+00	2	zhenyapopova96@gmail.com	3		11	2
68	2022-01-27 14:42:14.571129+00	1	voltovtom92@gmail.com	3		11	2
69	2022-01-27 14:42:22.582226+00	4	jenya	3		4	2
70	2022-01-27 14:42:22.586151+00	3	timofei	3		4	2
71	2022-01-28 21:22:32.935384+00	5	voltov-tom	3		4	2
72	2022-01-31 14:47:43.857599+00	1	About object (1)	2	[{"changed": {"fields": ["Image"]}}]	17	2
73	2022-01-31 14:50:22.801102+00	2	GALLERIES: Graphics	2	[{"changed": {"fields": ["Title"]}}]	8	2
74	2022-01-31 14:51:27.179005+00	19	19, GALLERIES: Graphics: Mark	1	[{"added": {}}]	9	2
75	2022-01-31 14:52:00.646865+00	20	20, GALLERIES: Graphics: DojaCat	1	[{"added": {}}]	9	2
76	2022-01-31 18:27:14.832874+00	21	21, GALLERIES: Graphics: NingNing	1	[{"added": {}}]	9	2
77	2022-01-31 18:28:55.164687+00	22	22, GALLERIES: Graphics: AvuChan	1	[{"added": {}}]	9	2
78	2022-01-31 18:31:33.608824+00	2	IN THE INTERIOR	2	[{"changed": {"fields": ["Title"]}}]	7	2
79	2022-01-31 18:31:53.606949+00	3	NOTEBOOKS	1	[{"added": {}}]	7	2
80	2022-01-31 18:32:47.388437+00	3	NOTEBOOKS	3		7	2
81	2022-01-31 18:37:13.941133+00	3	GALLERIES: NOTEBOOKS	1	[{"added": {}}]	8	2
82	2022-01-31 18:39:34.335262+00	23	23, GALLERIES: NOTEBOOKS: Suga	1	[{"added": {}}]	9	2
83	2022-01-31 18:42:47.030818+00	24	24, GALLERIES: NOTEBOOKS: Holographic cover	1	[{"added": {}}]	9	2
84	2022-01-31 18:44:32.466228+00	25	25, GALLERIES: NOTEBOOKS: “Y” keychain	1	[{"added": {}}]	9	2
85	2022-01-31 18:59:19.60037+00	2	GALLERIES: Graphics	2	[{"changed": {"fields": ["Image"]}}]	8	2
86	2022-01-31 18:59:51.645472+00	3	GALLERIES: Notebooks	2	[{"changed": {"fields": ["Title"]}}]	8	2
87	2022-05-15 07:45:22.268647+00	9	9, : : В чёрном 3	2	[{"changed": {"fields": ["Title [ru]", "Title [en]", "Slug", "Description [ru]"]}}]	9	2
88	2022-05-15 07:45:23.382444+00	9	9, : : В чёрном 3	2	[{"changed": {"fields": ["Slug"]}}]	9	2
89	2022-05-15 07:46:33.290443+00	24	24, : : Голографическая обложка	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
90	2022-05-15 07:50:28.142896+00	15	15, : : Вечеринка	2	[{"changed": {"fields": ["Title [ru]", "Title [en]", "Slug", "Description [ru]", "Description [en]"]}}]	9	2
91	2022-05-15 07:51:10.350976+00	4	4, : : Дождь	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
92	2022-05-15 07:52:13.410396+00	21	21, : : НинНин	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
93	2022-05-15 07:52:47.053181+00	19	19, : : Марк	2	[{"changed": {"fields": ["Title [ru]", "Slug", "Description [ru]"]}}]	9	2
94	2022-05-15 07:54:05.625309+00	17	17, : : VHS кассета	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
95	2022-05-15 07:55:29.255734+00	23	23, : : Скетчбук  с Suga	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
96	2022-05-15 07:56:24.703655+00	7	7, : : Нереальная	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
97	2022-05-15 07:56:52.607558+00	13	13, : : В углу	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
98	2022-05-15 07:57:23.369565+00	6	6, : : Ведьмы	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
99	2022-05-15 07:57:59.699348+00	16	16, : : ЛаЛиса	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
100	2022-05-15 07:58:52.266964+00	25	25, : : Брелок с литерой “Y”	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
101	2022-05-15 07:59:15.323223+00	18	18, : : Цветы	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
102	2022-05-15 07:59:42.838475+00	20	20, : : ДожаКэт	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
103	2022-05-15 08:00:27.250169+00	2	2, : : Рок	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
104	2022-05-15 08:00:50.292397+00	8	8, : : В тени деревьев	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
105	2022-05-15 08:01:40.60142+00	5	5, : : В чёрном 4	2	[{"changed": {"fields": ["Title [ru]", "Title [en]", "Slug", "Description [ru]"]}}]	9	2
106	2022-05-15 08:02:18.914314+00	22	22, : : Аву чан	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
107	2022-05-15 08:03:08.011022+00	10	10, : : В чёрном	2	[{"changed": {"fields": ["Title [ru]", "Title [en]", "Slug", "Description [ru]"]}}]	9	2
108	2022-05-15 08:03:40.493376+00	3	3, : : В чёрном 2	2	[{"changed": {"fields": ["Title [ru]", "Title [en]", "Slug", "Description [ru]"]}}]	9	2
109	2022-05-15 08:04:48.473839+00	12	12, : : Эй, девчонка!	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
110	2022-05-15 08:05:47.331075+00	1	1, : : Отдых под солнцем	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
111	2022-05-15 08:06:03.280492+00	11	11, : : Небо	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	9	2
112	2022-05-15 08:06:04.191285+00	11	11, : : Небо	2	[{"changed": {"fields": ["Slug"]}}]	9	2
113	2022-05-15 08:20:29.815519+00	1	About	2	[{"changed": {"fields": ["Body [ru]"]}}]	17	2
114	2022-05-15 09:17:20.772143+00	1	GALLERIES	2	[{"changed": {"fields": ["Title [ru]"]}}]	7	2
115	2022-05-15 09:17:46.570994+00	2	IN THE INTERIOR	2	[{"changed": {"fields": ["Title [ru]"]}}]	7	2
116	2022-05-15 09:19:47.930358+00	1	ГАЛЕРЕИ: Пленочные фото	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]", "Description [en]"]}}]	8	2
117	2022-05-15 09:20:02.359886+00	2	ГАЛЕРЕИ: Графика	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	8	2
118	2022-05-15 09:20:20.258461+00	1	ГАЛЕРЕИ: Фотопленка	2	[{"changed": {"fields": ["Title [ru]"]}}]	8	2
119	2022-05-15 09:20:48.930362+00	3	ГАЛЕРЕИ: Блокноты	2	[{"changed": {"fields": ["Title [ru]", "Description [ru]"]}}]	8	2
120	2022-06-29 06:10:13.108723+00	9	19, ГАЛЕРЕИ: Графика: Марк, Test123	3		16	2
121	2022-06-29 06:10:19.088132+00	10	8, ГАЛЕРЕИ: Фотопленка: В тени деревьев, zh-gallery	3		16	2
122	2022-11-04 06:17:19.54994+00	17	17, ГАЛЕРЕИ: Графика: VHS	2	[{"changed": {"fields": ["Title [ru]"]}}]	9	2
123	2022-11-22 19:22:03.675112+00	13	25, ГАЛЕРЕИ: Блокноты: “Y” keychain, voltoff	2	[{"changed": {"fields": ["Content", "Edited"]}}]	16	2
124	2022-11-22 19:22:14.262727+00	12	19, ГАЛЕРЕИ: Графика: Mark, voltoff	2	[{"changed": {"fields": ["Content", "Edited"]}}]	16	2
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	core	maincategory
8	core	subcategory
9	core	mediaitem
10	sites	site
11	account	emailaddress
12	account	emailconfirmation
13	socialaccount	socialaccount
14	socialaccount	socialapp
15	socialaccount	socialtoken
16	core	mediaitemreview
17	core	about
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-12-27 18:20:17.161381+00
2	auth	0001_initial	2021-12-27 18:20:17.748355+00
3	admin	0001_initial	2021-12-27 18:20:17.91175+00
4	admin	0002_logentry_remove_auto_add	2021-12-27 18:20:17.971545+00
5	admin	0003_logentry_add_action_flag_choices	2021-12-27 18:20:18.018034+00
6	contenttypes	0002_remove_content_type_name	2021-12-27 18:20:18.125377+00
7	auth	0002_alter_permission_name_max_length	2021-12-27 18:20:18.158552+00
8	auth	0003_alter_user_email_max_length	2021-12-27 18:20:18.178553+00
9	auth	0004_alter_user_username_opts	2021-12-27 18:20:18.192595+00
10	auth	0005_alter_user_last_login_null	2021-12-27 18:20:18.210549+00
11	auth	0006_require_contenttypes_0002	2021-12-27 18:20:18.21517+00
12	auth	0007_alter_validators_add_error_messages	2021-12-27 18:20:18.236762+00
13	auth	0008_alter_user_username_max_length	2021-12-27 18:20:18.271403+00
14	auth	0009_alter_user_last_name_max_length	2021-12-27 18:20:18.30085+00
15	auth	0010_alter_group_name_max_length	2021-12-27 18:20:18.331633+00
16	auth	0011_update_proxy_permissions	2021-12-27 18:20:18.356043+00
17	auth	0012_alter_user_first_name_max_length	2021-12-27 18:20:18.392891+00
18	sessions	0001_initial	2021-12-27 18:20:18.426764+00
19	core	0001_initial	2021-12-31 00:00:26.999227+00
20	core	0002_subcategory_image	2021-12-31 00:00:27.054571+00
21	core	0003_mediaitem_likes_mediaitem_views	2022-01-07 17:29:47.64566+00
22	core	0004_subcategory_description	2022-01-07 17:29:47.664675+00
23	account	0001_initial	2022-01-10 18:12:27.035825+00
24	account	0002_email_max_length	2022-01-10 18:12:27.077109+00
25	sites	0001_initial	2022-01-10 18:12:27.099428+00
26	sites	0002_alter_domain_unique	2022-01-10 18:12:27.138875+00
27	socialaccount	0001_initial	2022-01-10 18:12:27.411361+00
28	socialaccount	0002_token_max_lengths	2022-01-10 18:12:27.449151+00
29	socialaccount	0003_extra_data_default_dict	2022-01-10 18:12:27.466838+00
30	core	0005_mediaitemreview	2022-01-12 07:21:53.801845+00
31	core	0006_remove_mediaitem_likes_mediaitemlike	2022-01-18 16:13:20.416775+00
32	core	0007_mediaitem_likes_delete_mediaitemlike	2022-01-18 16:13:20.524904+00
33	core	0008_alter_maincategory_title_alter_mediaitem_title_and_more	2022-01-21 10:57:38.986629+00
34	core	0009_alter_mediaitemreview_options_mediaitem_like_time	2022-01-21 10:57:39.032278+00
35	core	0010_alter_mediaitem_likes	2022-01-21 10:57:39.060559+00
36	core	0011_alter_mediaitem_like_time	2022-01-21 10:57:39.083944+00
37	core	0012_about_alter_mediaitem_like_time	2022-01-21 10:57:39.116511+00
38	core	0013_about_image_alter_about_body_and_more	2022-01-21 10:57:39.146668+00
39	core	0014_alter_mediaitem_like_time	2022-01-21 10:57:39.170888+00
40	core	0015_alter_mediaitem_like_time	2022-01-21 23:42:25.278422+00
41	core	0016_alter_mediaitem_like_time	2022-01-21 23:42:25.304171+00
42	core	0017_alter_mediaitemreview_user	2022-01-31 13:05:03.870438+00
43	core	0018_mediaitemreview_edited	2022-02-15 17:25:18.176058+00
44	core	0019_about_body_en_about_body_ru	2022-05-10 14:12:19.099173+00
45	core	0020_alter_about_options_maincategory_title_en_and_more	2022-05-10 14:12:19.439163+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
b490ezsvrhx8o5w8in1orgiz6pq3lplw	.eJxVjMsOwiAQRf-FtSHyZly67zeQYQCpGkhKuzL-uzbpQrf3nHNfLOC21rCNvIQ5sQsT7PS7RaRHbjtId2y3zqm3dZkj3xV-0MGnnvLzerh_BxVH_dbKakXCeJTJgDaevMEIYLLwWaKTirTTCi0gKcIibQGgqM5gkxDJFfb-AMZVN4Q:1n1xOn:ipWa7mg0YB5sGO6Ncuj1J_fxjY_VKolallmZyr-I4fU	2022-01-10 21:19:17.405563+00
t1onbkoxfw59bzh9c6b749emrgb5s9pk	.eJxVjMsOwiAURP-FtWmQZ3Fnf4TcC5fQ2NBEYGX8d6npQpdzzsy8mIfesu-Vnn6N7MYMu_wyhPCgcgjYtgNPEMLeS5u-nVPX6T4SlbYGaOtelnP1d5Wh5vEzWyVmba0BAp60RBvjlUvAmBA5SHLkJFeISRkHMw6bknBKC7RGAbH3B8ulPQo:1nLkJk:siHqakT9OFl0Lv3XmUzwdQ-bgexY4Lj9PgfWUKbDIgs	2022-03-06 11:23:52.731954+00
lqh7utae8q7foqlfkfenvtxczofjwbgv	.eJxVjDsOwjAQBe_iGlnxb2NT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZaHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtHQIlY4gYCqeigrZeFbTjoMEkZ5wPXoHSwY4QhhLQESTW2jDlAADi_QHfWjdX:1n3B1Z:bBFFiNTluboEvEm6hXWQRltyXk4gMO08hs3pUikk4n8	2022-01-14 06:04:21.22577+00
9n5gzekrt4mkfutlre4i8v3zs5qlaxm3	.eJxVjDsOwjAQBe_iGlnxb2NT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZaHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtHQIlY4gYCqeigrZeFbTjoMEkZ5wPXoHSwY4QhhLQESTW2jDlAADi_QHfWjdX:1nNPdX:aGqPQaQMH27bmz0nkTGvGYdKNfxEzDOUCehhh9OGVD0	2022-03-11 01:43:11.899268+00
aoe76x5asdfw8iwj13tdbzfzij6j8qwa	.eJxVjDsOwjAQBe_iGln-xJtsSnrOYPmzJgZkoziRQIi7Q6QU0L6ZNy9m3bpMdm002xzZyBQ7_G7ehSuVDcSLK-fKQy3LnD3fFL7Txk810u24u3-BybXp-zYOgtc6BIJEPklU3SCT63qhQHujzYCDBKmw6wFFQmcCeFJKU4gIAFu0UWu5FkuPe56fbJRKIAjx_gD2gD_G:1nSilg:gdS8jLhRHTnLKzm8nFVmp_TC3-U-ChAcnPcz4zUgScI	2022-03-25 17:09:32.481516+00
r2prxqywcy7x96bqnsjamrkk5qhkyec9	.eJxVjDsOwjAQBe_iGln-xJtsSnrOYPmzJgZkoziRQIi7Q6QU0L6ZNy9m3bpMdm002xzZyBQ7_G7ehSuVDcSLK-fKQy3LnD3fFL7Txk810u24u3-BybXp-zYOgtc6BIJEPklU3SCT63qhQHujzYCDBKmw6wFFQmcCeFJKU4gIAFu0UWu5FkuPe56fbJRKIAjx_gD2gD_G:1nbHLH:Zc75q8MeZnxRr0gcjCm2QjbqUkmMZxPVBISpSEe-2Jg	2022-04-18 07:41:39.027579+00
8fwkoped3yx1cjvlo1f2ber5ec41blpu	.eJxVjMEOwiAQRP-FsyFtUVh69O43kF3YWtRAU9pEY_x3S9KDZm7vzcxbOFyX0a2FZxeD6IURh19G6O-cqgg3TNcsfU7LHEnWitxtkZcc-HHeu38HI5ZxW5PvgLElzRqQwdQwGq9a7IaWghos4MkeDZAKmuyGtbYaoQFio7CeFi4l5uT4OcX5Jfrm8wWpRz9g:1neDqr:t5Rr9yg-P9MIzev0oGonWkQm2DpDf37pKSh0y-7og9o	2022-04-26 10:34:25.94665+00
dqs9oef78jg2teg7coxtt7o6znhkt0m2	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiI4In0:1nh8Yh:Ey7ql4oJrnPYOWYhAEF8z7RjrZm5bfsplTIND2xaOrU	2022-05-04 11:31:43.303764+00
v7t26r9vpcs0bt6tmfzy31dx3o9dsioh	.eJxVjDsOwjAQBe_iGlnxb2NT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZaHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtHQIlY4gYCqeigrZeFbTjoMEkZ5wPXoHSwY4QhhLQESTW2jDlAADi_QHfWjdX:1nArFp:Ez9PeImFh3KeLTr9t6qb3_5bYWnIa-NGOxHvdoyMGyE	2022-02-04 10:34:49.337292+00
i7utwkmn8lfil1q486f39nx5sf5gnara	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJhIn0:1nhsIf:2Jvwdnn9qiYT2Qhhx7VNXbVGzp3Scuj6HL6IuL7ndHY	2022-05-06 12:22:13.505811+00
snlpep9wtingbs2tnyaff11sv638kf47	eyJfc2Vzc2lvbl9leHBpcnkiOjAsIl9wYXNzd29yZF9yZXNldF9rZXkiOiJiNGE3c2YtODIxNjBlMDIwYTczMDMzZTYxY2I3MmI0NTk1ZjA5ODgifQ:1nhsKr:5cXjDQP5xnvD0rPQ11-qDE83H0IKJJdetQNDjB-jKeA	2022-05-06 12:24:29.148974+00
wnx9gaqu93iqcu68e1m9xxxvbxgiq0n3	eyJfcGFzc3dvcmRfcmVzZXRfa2V5IjoiYjRhN3dpLTcwN2NkMDZhMWNlNDA0YTQ1Zjc0NmUxNmRjYjE4YmNkIn0:1nhsNH:528BQLMrw5am71X6jPHQcBT31dpMc-2mYLOM3hKS_es	2022-05-06 12:26:59.619096+00
i52latxx0gmx7x34omuoyiv99rdhci9h	eyJzb2NpYWxhY2NvdW50X3N0YXRlIjpbeyJwcm9jZXNzIjoibG9naW4iLCJzY29wZSI6IiIsImF1dGhfcGFyYW1zIjoiIn0sIjVBb0hDOFdjMExoayJdfQ:1nj8UG:ANLgO6v8T-HOUb7G1Ml-GeFstpOmmiSx8Nycadyn7yc	2022-05-09 23:51:24.459306+00
ai2rrichslg6okjtekoi111r82xchd2b	.eJxVjMsOgjAQRf-la0JobXkt3fsNzcx0kCq2hoLRGP9dMMSE7Tn3nrcAojiHyT549J1nZ_kGfhBtmIch-9s58ShawSITFuap_wHr3cKk3kMEunJYjbtAOMecYphGj_k6yTeb8lN0PBy37S7QQ-qXNyJWiozpQEmlsJOGHEKp64MsmqIiXRmDlWbSSjvpuprr0ui6IQQJsqE1mjglH4Pl592PL9EWny_n8lEq:1njJm7:n9KEZXrgqPht2r7F_B3Rm7higftOZF4Hg0d9Wptc6BQ	2022-05-10 11:54:35.81894+00
2g0kgjj1lzorajufderu0416jfrecv01	.eJxVjMsOwiAUBf-FtSFtuYC6dO83EO6jFjVgSptojP9um3Sh2zNz5q1CnKchzFXGkFgdVWvU7nfESDfJK-FrzJeiqeRpTKhXRW-06nNhuZ829y8wxDosb2vZGfS23VMrjSVEatC7DtzB05KBHqGPZLoFWmQDTM6DA3HAJopfo1VqTSUHeT7S-FLH5vMFx18_xw:1njJul:SvUviAq7-yqstcLFkxMZgjW4iz29BUJSbB-t3nxdMYE	2022-05-10 12:03:31.807738+00
05d4i0eku9hu5t3gzijyyt4yyo3qtzeu	.eJxVjMsOwiAURP-FtWmQZ3Fnf4TcC5fQ2NBEYGX8d6npQpdzzsy8mIfesu-Vnn6N7MYMu_wyhPCgcgjYtgNPEMLeS5u-nVPX6T4SlbYGaOtelnP1d5Wh5vEzWyVmba0BAp60RBvjlUvAmBA5SHLkJFeISRkHMw6bknBKC7RGAbH3B8ulPQo:1njncQ:Hu7ookAy8bbbB9u8cRy9jBQDFhaB6-kjRtRyOLaSZRQ	2022-05-11 19:46:34.197569+00
q70y9ov4bzkfzh28yb7abbcb51vjcnkz	.eJxVjMEOwiAQRP-FsyFtUVh69O43kF3YWtRAU9pEY_x3S9KDZm7vzcxbOFyX0a2FZxeD6IURh19G6O-cqgg3TNcsfU7LHEnWitxtkZcc-HHeu38HI5ZxW5PvgLElzRqQwdQwGq9a7IaWghos4MkeDZAKmuyGtbYaoQFio7CeFi4l5uT4OcX5Jfrm8wWpRz9g:1nkXSQ:bPvVox7BLpcPuY12TXQmRe_euhjJEYUB9qIVAuKIoWo	2022-05-13 20:43:18.70716+00
4syhlmf0q8hxfag367zg1j77by2j6544	eyJfcGFzc3dvcmRfcmVzZXRfa2V5IjoiYjRvajZpLWRiNjBhNWM3MTIzOTNlNjE3MDRmYTA2N2I0MzBkYWRkIn0:1nkg6M:TiCs1WGhx_e3TyiEmDp7jhYww3PFUN3ZNlyMac99IVA	2022-05-14 05:57:06.585151+00
a2qlvaj6m3l9zqx1x6i3sigfn8hrqysz	.eJxVj7FuwyAQQP_lZssCG5PgsXtUZa4qBAfEJC5YgKtWUf69UGXJdnfv6Ul3hxzRq1Uhxj0UmYsqFuaPO2wpos0ZZljjxQfoIGPcKoM6qr0sclNJfTUBHh28f2M48_F2nc4rfHYg_5U92yS9qc4BXm5a4c2GBsxVhUvsMYaSvO6b0j9p7k_R2PXt6b4EFpWXlh2cEYxYNhomhBsNOepBsLozNjHqmBPUojDcoNb0OFI3GCeQc82N0oepRXN908cg7c_m0y_MdCCCE_L4A9QqXbw:1nkg7k:izaGkGFwgZM8tpTHmhYjk9Qc6ViUcq39pTEWK9or46k	2022-05-14 05:58:32.623522+00
eivnf5trtoodftlftnzy6j4q7p39qx8g	.eJwVi8EKgzAQBf_lnYXQS6F-SC-lyLIsMTRm426EqvjvTW_DMHPClRNlYtattMkbNcH4OlHk2zAiRMpZLImHaFTnxB4Wsk_AgGrK4t6rrDGVbpy19h0daWvzVMlo-Qe4Buy3XZ90P9bjseJ9_QChJSqP:1nn0r5:mAAXooryyacSNL2GfTmM5nuz6dvfQCTcF-AzyGri86I	2022-05-20 16:30:59.94203+00
m031my0xwywci41a7t8sj8pcup1ejnrt	.eJxVjMsOwiAQRf-FtSHlNS1duvcbCAyDRQ2Y0iYa479rky50e8-558WcX5fJrY1mlyMbmWSH3y14vFLZQLz4cq4ca1nmHPim8J02fqqRbsfd_QtMvk3ft_GAQSlEgkQhCSv1IJLXfSdBBaPMYAcBQlrdg-2S9QYhkJSKMFoA2KKNWsu1OHrc8_xkY_f-AHx8PpQ:1noR8P:Pu7ls6eIsPpHSPYd_QIulSu6ofhKwh-ALubbiCue7r8	2022-05-24 14:46:45.787209+00
8w3shz8fwb3qwg6ejui7ileftdm5gd9o	.eJxVjDsOwjAQBe_iGlnxb2NT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZaHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtHQIlY4gYCqeigrZeFbTjoMEkZ5wPXoHSwY4QhhLQESTW2jDlAADi_QHfWjdX:1noRIw:IrKQ1YO6kKgqnbewMSW9eKvvYrUySoMtCI8UrA9JY2c	2022-05-24 14:57:38.030961+00
j8nqzhrtiwuir93hc6umm2nffj7stsef	.eJxVjU1uwyAQhe_CurUwOANkmX3PgGZgqJ1UJmIcNVHUu9dIWbR6u-_9PVXE2zbHm3CLS1ZH5dTbX0aYLrx2I59x_axDquvWFhp6ZHi5MnzUzF-nV_bfwIwy721KxjOOBAwe2bsuRpfsiKaMlG0JHg9hcp5sBgo7BgiAXntiZ7GPCossdY18vy7toY56Z1cU-a4tx8bCW7zwo5_pKbnzOxcsifigzWTGYqegdTGQKFhI3gCqn18zN1Mq:1nEXEx:ooLvm1_XTPcc6jVk417S-8MaWD9nF1phvlY0__0FYxE	2022-02-14 14:01:07.342638+00
26nn36djccogz1kqnbijq9p9p83k2yd0	.eJxVjMsOwiAURP-FtWmQZ3Fnf4TcC5fQ2NBEYGX8d6npQpdzzsy8mIfesu-Vnn6N7MYMu_wyhPCgcgjYtgNPEMLeS5u-nVPX6T4SlbYGaOtelnP1d5Wh5vEzWyVmba0BAp60RBvjlUvAmBA5SHLkJFeISRkHMw6bknBKC7RGAbH3B8ulPQo:1nEZMX:FUmj0ZtsVdgO7OjB7bFHFUMXKPC1Hi_mm69Im3krJBM	2022-02-14 16:17:05.257747+00
hz2na9fmxxesg01ee0v9wd6ceu4hlqht	.eJxVjMsOwiAURP-FtWmQZ3Fnf4TcC5fQ2NBEYGX8d6npQpdzzsy8mIfesu-Vnn6N7MYMu_wyhPCgcgjYtgNPEMLeS5u-nVPX6T4SlbYGaOtelnP1d5Wh5vEzWyVmba0BAp60RBvjlUvAmBA5SHLkJFeISRkHMw6bknBKC7RGAbH3B8ulPQo:1nHmeB:JPGvRPszIp28wusfMIP4JGnh9-x0_T3vjOmVzvxyQNk	2022-02-23 13:04:35.971267+00
489uxfhfzt62s6r1b7v8vs5kqm2uw2os	.eJxVjDsOwjAQBe_iGln-xJtsSnrOYPmzJgZkoziRQIi7Q6QU0L6ZNy9m3bpMdm002xzZyBQ7_G7ehSuVDcSLK-fKQy3LnD3fFL7Txk810u24u3-BybXp-zYOgtc6BIJEPklU3SCT63qhQHujzYCDBKmw6wFFQmcCeFJKU4gIAFu0UWu5FkuPe56fbJRKIAjx_gD2gD_G:1nInRO:YSgc-GXnTL3uNN3wK_C8sXy7yY9jI8e_sjalOh1RX9U	2022-02-26 08:07:34.505946+00
szhsabu76axnt1oc3suwg0p50h34uyvd	.eJxVjMsOwiAQRf-FtSHlNS1duvcbCAyDRQ2Y0iYa479rky50e8-558WcX5fJrY1mlyMbmWSH3y14vFLZQLz4cq4ca1nmHPim8J02fqqRbsfd_QtMvk3ft_GAQSlEgkQhCSv1IJLXfSdBBaPMYAcBQlrdg-2S9QYhkJSKMFoA2KKNWsu1OHrc8_xkY_f-AHx8PpQ:1noRvf:sxt7imWqc7Fw-_APDTlo6wVBA33QYYzpAdaMMlmsNzg	2022-05-24 15:37:39.057628+00
mu4ngicoi3kyy7yxh3mae3ahx7jidz9j	.eJxVjMsOwiAURP-FtWmQZ3Fnf4TcC5fQ2NBEYGX8d6npQpdzzsy8mIfesu-Vnn6N7MYMu_wyhPCgcgjYtgNPEMLeS5u-nVPX6T4SlbYGaOtelnP1d5Wh5vEzWyVmba0BAp60RBvjlUvAmBA5SHLkJFeISRkHMw6bknBKC7RGAbH3B8ulPQo:1o10td:BjZOgYhFGA62nLbU6iZb4-vQFN_tkxzSMdIYKDo-nlU	2022-06-28 07:23:29.827959+00
jp6js427zvks1pl2fhv9ek0577txyqub	.eJxVjDsOwjAQBe_iGln-xJtsSnrOYPmzJgZkoziRQIi7Q6QU0L6ZNy9m3bpMdm002xzZyBQ7_G7ehSuVDcSLK-fKQy3LnD3fFL7Txk810u24u3-BybXp-zYOgtc6BIJEPklU3SCT63qhQHujzYCDBKmw6wFFQmcCeFJKU4gIAFu0UWu5FkuPe56fbJRKIAjx_gD2gD_G:1o6Qsz:D-8EhV-6Z1-q4xDDGE4770rJSsZQ0GpqhlhSpTAUsWw	2022-07-13 06:09:13.736991+00
w7kf2airvaqb3uuki0elie8kn5chfmu3	.eJxVjMsOwiAQRf-FtSHlNS1duvcbCAyDRQ2Y0iYa479rky50e8-558WcX5fJrY1mlyMbmWSH3y14vFLZQLz4cq4ca1nmHPim8J02fqqRbsfd_QtMvk3ft_GAQSlEgkQhCSv1IJLXfSdBBaPMYAcBQlrdg-2S9QYhkJSKMFoA2KKNWsu1OHrc8_xkY_f-AHx8PpQ:1oADEU:J5IHQodbXo5h48AvKXMYIfytSf4M4fSTuefh93PtkqE	2022-07-23 16:23:02.441457+00
br9cf6w5m5au6qsskmphgfbihcmc4448	.eJxVjMsOwiAURP-FtWmQZ3Fnf4TcC5fQ2NBEYGX8d6npQpdzzsy8mIfesu-Vnn6N7MYMu_wyhPCgcgjYtgNPEMLeS5u-nVPX6T4SlbYGaOtelnP1d5Wh5vEzWyVmba0BAp60RBvjlUvAmBA5SHLkJFeISRkHMw6bknBKC7RGAbH3B8ulPQo:1nqAS6:LeY99DfC0rcU79Mxmtd57sKTiR9dUCvUby4X90rcecE	2022-05-29 09:22:14.984873+00
gpb0xzny8mxg43zi6zoyzaosspauch5j	.eJxVjDsOwjAQBe_iGlnxb2NT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZaHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtHQIlY4gYCqeigrZeFbTjoMEkZ5wPXoHSwY4QhhLQESTW2jDlAADi_QHfWjdX:1oG2vQ:BCVGC3wQbfF3m75Ky3xKWvFRXN22OgeRoljObVKy3Ms	2022-08-08 18:35:28.280641+00
ke5o8jijpbgec6uulvpnjkhn14b0tjlw	.eJxVjMsOwiAQRf-FtSHlNS1duvcbCAyDRQ2Y0iYa479rky50e8-558WcX5fJrY1mlyMbmWSH3y14vFLZQLz4cq4ca1nmHPim8J02fqqRbsfd_QtMvk3ft_GAQSlEgkQhCSv1IJLXfSdBBaPMYAcBQlrdg-2S9QYhkJSKMFoA2KKNWsu1OHrc8_xkY_f-AHx8PpQ:1oGHU4:o_BYuEmDHPX00d7ltJKJOIhWSwaPTg0EmyQynPunFNQ	2022-08-09 10:08:12.999108+00
5hf3oo11jfodygd1pz2vzy4c0ouatmeg	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJnIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ:1nrvor:8og58HqnMrMSXemfmp63-09J2cBwZwLrxxvY_tSeh1U	2022-06-03 06:09:01.378194+00
ovne54nci8qe9lshzwuphx20f7i6xhhs	.eJxVjMsOwiAQRf-FtSHlNS1duvcbCAyDRQ2Y0iYa479rky50e8-558WcX5fJrY1mlyMbmWSH3y14vFLZQLz4cq4ca1nmHPim8J02fqqRbsfd_QtMvk3ft_GAQSlEgkQhCSv1IJLXfSdBBaPMYAcBQlrdg-2S9QYhkJSKMFoA2KKNWsu1OHrc8_xkY_f-AHx8PpQ:1oLgxc:17XRWucUVAmZyfw4KoidpCkTFvaRVA0Egj6NOS5dIzU	2022-08-24 08:21:04.49091+00
2xxhv7q9wuh1xxui6qcy52avi9zzyxsf	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJoIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ:1osXHu:jdJNlEGY_7f_cUeMYvOt1FGKEV7zaNu8lfeSxq9NYxA	2022-11-22 22:41:46.427988+00
r1ykgwk2oomt98kme59d85hcav2rfikm	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXIw:OQS8FNLzVuxe1cD6SO2ZXFMGidSCmxvX8Xyvt1y5WH4	2022-11-22 22:42:50.493959+00
os3ehx0og5i7wd9uxqx5zt5mduncd5r5	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXIw:OQS8FNLzVuxe1cD6SO2ZXFMGidSCmxvX8Xyvt1y5WH4	2022-11-22 22:42:50.706059+00
ippz8wq1uyb6fn3spvi11vprjebl9s9k	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXO8:_1wdXhMSZyLgBDuG-pBBufTQ3nfFy6poaSY9T1jHzLA	2022-11-22 22:48:12.924193+00
rzqibduu7z392fww2c4137cz24g6950g	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXTM:DU2mhEMkJKuqVmFUgBnMTrGaXCMPeSkIJQEJxwmtaDg	2022-11-22 22:53:36.82823+00
o6z1ku5vdkwej5kavlqkoc3c1zkvo80j	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXYa:TIv9tWAm1h5W0B170_LlraMkGA46QR_TOG_dF1ubjos	2022-11-22 22:59:00.281672+00
jbceavdiieng6eicwqv23eji6ww2jcvj	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXdt:SUIrPlwhApy5bLFn3sBGPC8ruCK9BxG1CkK63IeeiT4	2022-11-22 23:04:29.45956+00
000qe8u6eq91rui0vj7i64jrm1gngzq4	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXjC:5cH235Y4D40ToAavOZ6XkjghdYr3RclR_IJ7vcEy8tQ	2022-11-22 23:09:58.16476+00
epdj80uf831lawj7um1ot6kcs027yjgn	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXoO:jWkXMG2yfi4fnIRXx5RPu2Jx7S_5iY5p5zDPjBJwX_U	2022-11-22 23:15:20.551923+00
lxhymlnwx107u87bauw34h8yfrz9z4wb	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXtf:FwJesm-rHgxEWc5wrS5z9tuctbcZnGZOs4-7F9GYSyE	2022-11-22 23:20:47.92082+00
mg42rnm1gfgndvocag9cvjnyrb3qaj1u	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osXyu:etREbrOsM-dN_AgEKGuxDw0K8Usj9MF91x1kDKAyBmo	2022-11-22 23:26:12.565347+00
ji9uugn6fpazw3sv59mkxoey8rwyy2yq	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osY47:uvYMP2Lf-ZhkBsdmQEgxqOljYkPjrGGxZcQdKoGTMpc	2022-11-22 23:31:35.318252+00
gmg7ks4571p95nlko2kcbkgn120pgmi2	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osY9L:QzvBHDtfwyH4yYKvD8b2xJviIj_HRKqKUYL2GQ7osok	2022-11-22 23:36:59.541609+00
ruft6frrpfn1fo17j1wpe0hoczs9n8jd	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYEc:HaRrSzlkjweme7pqJMLwT0NVzsjjNlOI9DPzGc_A0-Y	2022-11-22 23:42:26.54912+00
cn4pwxhb1s0v3llt0uxtyzgz0pixdkk1	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYJp:KEpfWI6ttqYsMdNntSCQ-P6TtemFhslb5npB2Fg8vLo	2022-11-22 23:47:49.349895+00
oultu88s6w7t9xhjzav5fneqr60m6c6j	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYP2:H-nWMXYhz-1bJ2jS5UUUVFtuVuvrL1XN70RUzj_VQjw	2022-11-22 23:53:12.561634+00
qtsur0y8i52ochuvzjeduzttwz5vz6dc	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYUH:zXUaV9Xhre_TPA3fR8rlnD6XYMskMMbRIx3Yc8bNLIc	2022-11-22 23:58:37.05265+00
fm69ezug23kxmynthxnxwhmcfjn0frz0	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYZS:hyi48Gj63_u0aoorbBosdQ44PPFMUZZOZnqwfnU5oU8	2022-11-23 00:03:58.464362+00
d7jxscta2iww4sby1k3w7b3fusuxzdpq	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYee:YOjahBlb6Jtk-bUnQMDpustFIhIGn4TehL4bd_8GYT0	2022-11-23 00:09:20.095342+00
msnjaik7a69leiztu4bg1qjw6bk1qqtp	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYjo:X3nGbUOCnfhKv5nBNw-dd6No2ewmU4_nqcs9n5UyTvs	2022-11-23 00:14:40.623781+00
oyx9wnm55g7hvovm8wavdng7zq7uz6yo	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYoz:5Nxh7pRyAyCpUY7nEeo3D_HNtWftKV50-q3obQGBj1A	2022-11-23 00:20:01.811097+00
381xm71ttu77y46kevjsh4bxz9zol4uz	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYuD:lYyCl19A2bwJyzi0K6V0skCx4-86Sqq1SoZIZ6gJJtI	2022-11-23 00:25:25.248728+00
bbmg8gh745njx84i6ws2j2k1ykq7dut7	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osYzO:n6HTyAMNWBkOc3cUN1yoIrdp0kCDydC7UY0rPAXZXIg	2022-11-23 00:30:46.221519+00
1wi831uhw7v610w4xb66ea6jupaz1u9p	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZ4c:cRVdHcle-mUE1-Q6iKIa4qWhHA86bgGvYwjYMsMHw3Q	2022-11-23 00:36:10.405151+00
zpv3szevexehe748v50ccajmjoqbok9r	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZ9n:ioUudqm9KWAyyoBT69IUK5NlPuJAZD-VH2hQ5XSgNDA	2022-11-23 00:41:31.973465+00
n5l76iyf0tmbdf2cwe9cj9vwwhd8lifd	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZF0:cOwYmn6cEDKRPsUrW5i78FK9CRlsm_4_FD8qoZoa4vY	2022-11-23 00:46:54.561608+00
gx3boplkzxqsnqz80qhbel466mkeqhic	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZKE:nY0_GncY8HgxcCJfCq7MUWj3WzHl4cgyUzCmsrkbs0s	2022-11-23 00:52:18.330948+00
7jznzg3oq1g993itbz0t569m9q8x335p	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZPS:P9vkfayRYdseyC66nTtOWrT8gXv0WI2cgor8Z4DfIjU	2022-11-23 00:57:42.702453+00
egv8n3kenfx3q4beafw7fm6m46b50qut	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZUg:X6IIwQquWrvSMWbtU2MeBMEwpIO2JwehOTQrLX6gvUE	2022-11-23 01:03:06.146649+00
64hpnxi74owkfprc2cediqdr020lb6xe	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZZt:tpZkSRC3KhY1OKiBZ-H726I5bugiwc8m0g4XJz2YKjc	2022-11-23 01:08:29.491975+00
xujrw94vtinmjyi4nagksf7b7angtm0x	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osZf6:ZOK7nmAb4XeQ1jnbHCi6yOpaS1w8VU9LEIbj4lilx5M	2022-11-23 01:13:52.95222+00
kedm0ppta9lhf3pf3bgs4tfepcl293rn	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osgyH:aUVLF6fR3ZeDnkGUedqnx62UEsKBfkJN8fITjksLbsI	2022-11-23 09:02:09.920327+00
s3ruyl6l5t1tq4vv7crfgbeyuags9a58	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osh5l:xQgHcjalFZ6Zsw0NXsRWAaYmEEzNNTtjR5HtGXiFBVQ	2022-11-23 09:09:53.535782+00
dfzq4hwtt7ytii5qdu8fiz1khzxug4h2	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshB3:-VRyct0fX7eyMv6vZyb7OncTw2juLaMIDQnIVk9nrkc	2022-11-23 09:15:21.285479+00
sino15qnds016nk4tvr1mnozp9sowbxp	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshHK:6xfsMipv-mRFbRePfkAKnhOODqPBrEuxPYokM2BM1G4	2022-11-23 09:21:50.84292+00
7vsa79rn8k2inyuy4vle2kx8f8u1dic7	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshJr:jamdYXlu4hojSfdcWWtj6Y6UMbl5PhDGZO8AoTGGXps	2022-11-23 09:24:27.46874+00
yltu50166fm7fuztee34laueem92cr1i	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshK3:i4yfaXp_2k76v1BO9268zSfqyDLLEY0J1qu6SBwcYew	2022-11-23 09:24:39.168731+00
wwohkr22hmy490mpgv0q87bkgvxpqd0r	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshPD:yGb_dfimTTKc22eQnCCy_swKM_xvFNxCccYJfP-Up1o	2022-11-23 09:29:59.08073+00
4l7pmfibidzkwhi41to566w3jg8rgd8h	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshUR:jVC-tIx-eT9Q0z07byU5LLUGsBUz-1HipVKVxdC1C9E	2022-11-23 09:35:23.194886+00
ciocuymhofy8upewfmptd587sky615lb	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshZj:dw0H9-zq9AyANALW3jZpVglfUDn_erPLzxlfF77Em2A	2022-11-23 09:40:51.488308+00
xbxdcq0c4j8g8rhuhaby01pyemx01ns1	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osheu:oQAQCnNZ0x3dMaseG2cDV25q3_hReE8pn39n9Xik-wU	2022-11-23 09:46:12.185154+00
g8t0xd3jtoxqvqgr9vufabs7bwnwwnzt	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshk6:H-XukLEjDGeNMAmBa8Num3DDYuA4CtHCfzlJ4-v341U	2022-11-23 09:51:34.578756+00
ua1txv4rmpmdbr2twzslei84pvj9xcmk	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshpG:-Ft6I0U1LQ-771iMX-xBbE_6SHtpQ6Ifhb-rFU_CGHk	2022-11-23 09:56:54.910545+00
a5vx22riks0rkkhx5rovr6eeh74fmf2h	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshuV:vTHsSs4ctJ-axAwjRoBTJ5Uli1ghUqjF7putPD1q43Y	2022-11-23 10:02:19.711201+00
j126h8lc4gkagpfw95jognn215o5gmoa	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oshzg:xOzBdDXR0GHsp7WLiWF1DUnCv98nmTqxN4z2EncTQ3Q	2022-11-23 10:07:40.596445+00
efhdcvirhu8q5k5r8xpxxacdgs6qgwo6	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osi4u:Gw8Ow-rrW4QJYwcXvcA8K876nHx91vZqAXdOXQ-dxHs	2022-11-23 10:13:04.038029+00
qxe4unsry6mlubzdva2vfyiiq8wl77ix	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osiA5:OZ9vuAi4vXeCxZqXW8G_A04w-JhR1VMWgUZ5txvCLus	2022-11-23 10:18:25.658564+00
2gwruf3nl1rhb0ajtwumq67a17ymwxwz	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osiFH:G7nRkxSsHTFzvIgLAwgaAVNP6iKxNMg2apRzm_xsOeg	2022-11-23 10:23:47.134417+00
ch7o1d24yysxgkadrs2t353y1ctqe3o5	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osiKV:KuKby1uJlFW2dyPXMd3BbbYcArkehA7NqqmgpIer9iU	2022-11-23 10:29:11.974622+00
77p81vbe1mvdgaop01e8ehw9g7dte2v5	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osiPh:dJ-Ilkh1Rxf4BW_pACqevn_EEvsGmI9VGYkhghytn5g	2022-11-23 10:34:33.678652+00
l9h8mxg2tc8ff6wqmbdhbwjaw2kcxvll	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osiUt:rfIIZtcA9WH_3-pm4A8gslKli22ex3v2-pT_KaL6N-A	2022-11-23 10:39:55.856369+00
s2qj83prqx30y4ny8nd695s4yaeb2dw0	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osia6:6ir4ih39LCZEQ5GAZL0fSrgcdaPlbTkRFb1sCcNhipw	2022-11-23 10:45:18.018927+00
s2ebie6wpf6h9afe10vnfabz10a923zg	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osifJ:7JcR0LpbrE_4zMyi631ogvJxg9D1G-LZC_DiXfi29i4	2022-11-23 10:50:41.252865+00
d37t0d5hccrah5rdase5igt5je715ihr	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osikX:E2I6YBRs8NozcfWpbAI6rWUaAuErFn4p0ZBaxbMwy5o	2022-11-23 10:56:05.553023+00
azet4ge9fnjg5y90gd57etcxki843fk3	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osipj:CNekEB86LUmVe4GnNZcTGcUlKiQWRNWfFZaQ3xhJAEg	2022-11-23 11:01:27.272773+00
8rnf55hyq2d2vsvl13dyigd74h098p2z	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osiuw:9hchmiqrTrjySd8Kh0_BYwpljrVzXQLL2ok0Ns49UPU	2022-11-23 11:06:50.188733+00
akq09p9jdaaj5llwqk4s3vvwccxma0g3	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osj08:ebXIoWchsl543pRgJb-dqFsPReErOaWZijgSNEPiCHo	2022-11-23 11:12:12.823988+00
xl5y8pv8ox71wx7ixwr34g3tulrof3uh	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osj5L:o-0sIt3SogvW-PqjSP6q-O7v1JHidzJ9QB8YhrmVt5k	2022-11-23 11:17:35.521086+00
kunvuvyuj4srkiy5w8ktf6m0b6n56fh0	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjAX:uHt56fGHMWeGE8z0m7ydt92vcfUQIqjC5s4zhdupFUI	2022-11-23 11:22:57.391233+00
6dyqoh4xe3dylucop37ecsvi3qd7drfl	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjFi:j_SNDzm_en2mhuNnAe9hkqrfMuTohkhY1z0R5AKJeBA	2022-11-23 11:28:18.174746+00
j72a3x87axgdeiih8ln5kbkciuo7u1yc	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjKu:4u6_Ma34Oj_G_ZOIizfgYeftnWyNkwOq0R8tPT-5huM	2022-11-23 11:33:40.913+00
8vyr24bjgn84za9vvo3oahotjo671elh	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjQ7:FGqvISH4Tod4FkPfh40I8CiAbxu5-r89vK6GmNZzeM4	2022-11-23 11:39:03.816395+00
ff3w5zk4qkxvx5vszmxsr8gr3b7f3ebe	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjVL:vgmbGoZeVFQIKSswJgg_lFb5ShYuezFMOgRcT_r5cls	2022-11-23 11:44:27.616202+00
laayq01ojcdq70zon6a1oshhl9k4c1ma	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjaW:6_UgJqJChv8okmvvVk7L0oltb5o7ZWImGezTLPRn1Rw	2022-11-23 11:49:48.659463+00
4bg81yl7xjvx3n1ydqnhoze7deshfq57	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjfk:HjTRWT9bA1ikbcAQ18GjQiTX0n-lIQgRptRiU-9R6oQ	2022-11-23 11:55:12.917293+00
k9yy75gyen6zrw8eeene7tu1vjvfie35	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjkt:1nNtqnSUpMtzZHqcJhCgm7YiWxWilQF9G05qrpXT7iI	2022-11-23 12:00:31.760021+00
iz8pb35gh05yes64skjw0ngkkcjytmvs	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjq4:L2f85nM0C2V3EsfiwxCFX25q1XqhUbyDlIR_Fz5i7R4	2022-11-23 12:05:52.687699+00
6t1jsfwyt1nl0he7x585ella9xgi8f6u	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osjvG:luXlUqsEpGziS2_QJbZE74I1nbe6FFZEWGxsZW9zaOk	2022-11-23 12:11:14.210962+00
q9j2nr674tsyqp3b01qmbo0bcr5fsn9f	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osk0R:rVhNLL3H17D6mWkUeSmgVRjvopM_qAmraGSfF_mCvbM	2022-11-23 12:16:35.159317+00
kqhsf9hyns1xvfb3rzy4ywzbtr9s9qcn	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osk5c:OJ2G4ADzxZANueoKb_U3KeQ0O4NHTh44-rjlOBzmLW0	2022-11-23 12:21:56.548736+00
nwdwzqa2q7ktxt3h0zfkbb8pdzns6786	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oskAp:fFsh_JoYhOMs3A8cfvbd_nYzWlRnYJopmDWZkKhjWgM	2022-11-23 12:27:19.792338+00
31p9dacnmjbjyzhtwwhir37upts0ramp	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oskFz:Xj7BzL3aa_IKQRzRncVMEZTKUqTenjho31bE-q299lI	2022-11-23 12:32:39.258322+00
1t0cdhs9xka736x45k70j3mtv6009kzy	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1oskLA:9z-6lTGFET4SUAMIV20rXnolPm6BfhvprHlTdvnym08	2022-11-23 12:38:00.015809+00
4htshept36b9hu6boyj3zidfw0flubvr	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmDm:77xGOKT-SWAEIIspHoAx1ZW-6btyPPV5Lx3it2uRcOU	2022-11-23 14:38:30.387314+00
nol3fzlui73szi5j93qfz4rktao9c2pu	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmJb:TxxSA8XBca7XEW7-Xq-CQHiQ1TOIL3TUiCx3Cm-9Dz8	2022-11-23 14:44:31.402433+00
vcnmahcc4lz5sc43alkpnvevtqa3qb3y	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmOs:C-XGKEdeqSU2lCDFxg2AYqhUnY5iOyS4UFxwxzH3xVQ	2022-11-23 14:49:58.793123+00
ifydi2h4o18jwaagjk4sbcrklo4vh4oh	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmU1:mapmPET-4cP54zbP62Vf8iHivh5uNmujTVj9YWP8SpE	2022-11-23 14:55:17.02484+00
5uf2sht4n2g2nfcwla6cps359g6927ck	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmZB:A03wNvZh3wFqgSw-a1HbCK-0ykZMCymE39bx3Tqe3oo	2022-11-23 15:00:37.98356+00
0u13tr80c1yao1qxy5hgejbqs3ubz0tk	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmeN:wxTuiMlS5ptmQj1hMnypFd_p0bmYVgQ1rS239FtBWw0	2022-11-23 15:05:59.073816+00
mdehw3as9s9pobq2yjgtd1t1273qoxxz	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmjc:ptZZLVpLStcyAMUYdPKNs93lqqkNnygGDRAfbVxiohk	2022-11-23 15:11:24.116323+00
pcbcrovw1zbwx2mpjw4cg8hgnfkcnb3w	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmoo:sm1F0JQHdquVjmxn0VFr4dEOyyO041zs5jw8zVi6pns	2022-11-23 15:16:46.483233+00
fycbsqa6i0hxsdlfu8soeoywalv9lkcv	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmtz:MCo94yET060BpkODgbR9sPl_NQWA5kCux5-gK-GVuvY	2022-11-23 15:22:07.98929+00
qqpdjif25o692xavsp9c84gjg5m2ozgi	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osmzB:IethntA57aaHbGRrpJDS_4J0IVwrtpwCxr29cK-9kYo	2022-11-23 15:27:29.435433+00
etiy84h0ftovtn4010jtxwl9yt9e6l2u	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osn4N:2qohVlArkuyPR2QX2aThmtdqKz6A-cJY9VEF9Uvya1Q	2022-11-23 15:32:51.153937+00
wdhvj9dat4agsr0k97gmh5a1vbtpqlv3	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osn9Y:EP5eOGePgVu6CkU9ULYpmcRD2FccQxzyVgmSTdUk2R0	2022-11-23 15:38:12.683504+00
dysob2nhb4hkkp4p8jp7tgtnqxjsvmt2	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osnEk:SuPwVsb-vLs87ZAVISdG7OVoYzNB-uzUeMy9hQ5Hnco	2022-11-23 15:43:34.215+00
vixexd0wvz2c7yj1fkt6kfkn4ciedkvl	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osnJt:OFlck0WCFtPsTIzQuDmzB-7fAKhml87Br7KJyza8vZU	2022-11-23 15:48:53.990474+00
j4nyysgelck2r5bo21ezwap2btnki2l4	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osnP5:FBrASphpFFh9ubVnHKePap_OYcRIb9HMAN6ILcFjLbg	2022-11-23 15:54:15.978738+00
rsdnan8ciblt376vxaem3gy98hsnmdiq	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osnUJ:adSzAYb_lk7ysakox3agarBiZ3cKKNlUmFvEPify8Y0	2022-11-23 15:59:39.135743+00
wnvd1hue5l0014wcv039wxb4bupuf9sj	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1osnZV:OOj8URaEX_JYL7CqwbSOa__kIP51WsD4lqwSGRdkALo	2022-11-23 16:05:01.171855+00
f9ow5dlpgt2n6z2jtnd4lllcj3xnszz2	.eJxVjDsOwjAQBe_iGln-xJtsSnrOYPmzJgZkoziRQIi7Q6QU0L6ZNy9m3bpMdm002xzZyBQ7_G7ehSuVDcSLK-fKQy3LnD3fFL7Txk810u24u3-BybXp-zYOgtc6BIJEPklU3SCT63qhQHujzYCDBKmw6wFFQmcCeFJKU4gIAFu0UWu5FkuPe56fbJRKIAjx_gD2gD_G:1osoc0:e93imVH4QpxyeT4DI3c_qWrABgWkRGWJLpXn1PGn3dg	2022-11-23 17:11:40.911366+00
0b8rr04cv0rtq7vbiml8i1rx3t00qfww	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJpIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ:1ovYgM:fYVYK1p68N_sS2JOQBrQD-UA4Sy6mhz6QVTD7RuLj0s	2022-12-01 06:47:30.705478+00
409l80qrwjs2pe5x69mwbzcoml0y0ein	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1ovYhR:n62YvBmC-hy7SYjGi55rtD7i_sbVjeCA61WbGdArkkw	2022-12-01 06:48:37.408662+00
ergrhpk0rqqbpi4mj8dx8fj2nxdshfqz	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1ovYkB:gSSEsmooyh40bX76ToO93Mt0zk8fyCaJDDcSIYejn1Q	2022-12-01 06:51:27.949388+00
3cfw1mp8sqjo9d84h812pxjt2dkooep3	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJqIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ:1owDwn:sHxismxLuAE3Deguw1xYuH1ovxVfzw8xCJOT3LBFc3Y	2022-12-03 02:51:13.100252+00
9982raqg2fqroav4tit9qo87aprjgf2k	.eJxVjMEOgjAQRP-lZ9O0hbIsR-9-Q7O0i1RNSygkGuO_CwkHTeY08-a9haN1Gd1aeHYxiE6gOP12Pfk7p30IN0rXLH1Oyxx7uSPyWIu85MCP88H-CUYq4_ZmT8zG4tAa0AMF1ICVVbUO2teWAA0Qmi26VlXAxnirGcD2rBoboN2lhUuJOTl-TnF-iU4bhY1Sny_yCj-X:1owz7t:OtA2NmXWUP3GPn219DFAGrKmpHoxHxWPygP5CD1tGQw	2022-12-05 05:13:49.167468+00
220ek7q6vn3bgvonpdrhqgkmif06zua6	.eJxVjMEOgjAQRP-lZ9O0hbIsR-9-Q7O0i1RNSygkGuO_CwkHTeY08-a9haN1Gd1aeHYxiE6gOP12Pfk7p30IN0rXLH1Oyxx7uSPyWIu85MCP88H-CUYq4_ZmT8zG4tAa0AMF1ICVVbUO2teWAA0Qmi26VlXAxnirGcD2rBoboN2lhUuJOTl-TnF-iU4bhY1Sny_yCj-X:1owzc1:YCSEia-8C5TSB84j41ugLR-Kuzo00GYo3sc7Ikswr74	2022-12-05 05:44:57.991124+00
4a8b763j42vzprhbln2sxe11xg2e1pmf	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1ox52o:hpb98U7BsAguWEX2aNqI2gAPzdkf4-b_XSP7mZq7JtA	2022-12-05 11:32:58.151338+00
zlk9100fig6qr0vg1vb5z9di406aypcn	.eJxVjMEOgjAQRP-lZ9O0hbKUo3e_oVm6i1RNSygkGuO_CwkHTeY08-a9hcd1Gf1aePaRRCecOP12PYY7p32gG6ZrliGnZY693BF5rEVeMvHjfLB_ghHLuL05ILOxbmgN6AHJaXCVVbUmHWqL4AygM1t0rSpyjQlWM4DtWTWWoN2lhUuJOXl-TnF-iU59vnkgPmU:1oxosK:TdkVjtg3gr4LdDYNUW3L8kuBG_0h-_KMQiMdCJZWl_c	2022-12-07 12:29:12.540607+00
angs43m64bsui0qpscwiw4x6z3rqte6j	.eJxVjDsOwjAQBe_iGln-xJtsSnrOYPmzJgZkoziRQIi7Q6QU0L6ZNy9m3bpMdm002xzZyBQ7_G7ehSuVDcSLK-fKQy3LnD3fFL7Txk810u24u3-BybXp-zYOgtc6BIJEPklU3SCT63qhQHujzYCDBKmw6wFFQmcCeFJKU4gIAFu0UWu5FkuPe56fbJRKIAjx_gD2gD_G:1oz2W8:XPIyWFRGGkVbNyhqW30Ln70bq3AA1b-Pwr-ZAEwnMcU	2022-12-10 21:15:20.895157+00
iz4wrnmy2plmbyeznp4hajwygt19otlc	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJrIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ:1p2MOH:xWvfheWfPECJKEvhlln_b8kB_yyW0jf5U_nI6DLFwgU	2022-12-20 01:04:57.831732+00
krcymfrfe3uaooav5lngb6rlox11fev2	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1p2MTp:724NUJ2h71iwg9hvVh42ouVaOgQ5r3OvqGSWDqXGXtU	2022-12-20 01:10:41.946018+00
2wd6ykksiuhx2twu4y2pvs0kthima2s4	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1p2MYr:K20kZtECbSZB9WPHXkbVSy9hklqevVREg6rklAZBXdw	2022-12-20 01:15:53.579802+00
z19fv6rsp38brtqwwqgnore6cvw2ksuc	eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiJsIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ:1p8hsr:1iGv0Ih9kBNOuTxwPLWZ9TiSNFXzfb0lUHW__vRhD0k	2023-01-06 13:14:45.603614+00
j1fvb7awev1gpium9jrpxsg0g8hu1n8i	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1pA8Kr:Qb-BeXzAo32DJBrxeYCXAJzEMV5aLvAUj_DPGr2Udlg	2023-01-10 11:41:33.591081+00
zqc7wb7o554o1lte5gnqlov88ttprslq	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1pB3kt:0rlaktbO9QP0_FOJxTXqKO2zWP09vurfhs_O5uILstg	2023-01-13 01:00:15.329985+00
kz4lhl8kqul5u30t0kt3zojtcaocvf10	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1pCHsE:S_LqujnuOdUScaEl-5s3YM-xwmwKDglmGGRkFmtZw90	2023-01-16 10:16:54.21755+00
9nsan76xai04hqgfn83s9p08nh0u4u36	eyJfc2Vzc2lvbl9leHBpcnkiOjB9:1pDRj7:s3_vlVtsiJqJa5hfWFqHfBLmLDufw4n4RvjKDcbsjDg	2023-01-19 15:00:17.458608+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.django_site (id, domain, name) FROM stdin;
1	zh-gallery.ru	zh-gallery.ru
\.


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
3	google	104890244786077332574	2022-07-20 10:29:28.761994+00	2022-01-28 21:25:06.922211+00	{"id": "104890244786077332574", "email": "voltovtom92@gmail.com", "verified_email": true, "name": "Timofei Voltov", "given_name": "Timofei", "family_name": "Voltov", "picture": "https://lh3.googleusercontent.com/a-/AFdZucpSHzOo5BlwW-Ohc-roRx5B-3g0aSfS0nQoOT17ug=s96-c", "locale": "ru"}	6
\.


--
-- Data for Name: socialaccount_socialapp; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.socialaccount_socialapp (id, provider, name, client_id, secret, key) FROM stdin;
1	google	zh-gallery	412447480251-vvqq6rnnk06494tq5cbb9qtu9l4m73u9.apps.googleusercontent.com	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	
\.


--
-- Data for Name: socialaccount_socialapp_sites; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.socialaccount_socialapp_sites (id, socialapp_id, site_id) FROM stdin;
1	1	1
\.


--
-- Data for Name: socialaccount_socialtoken; Type: TABLE DATA; Schema: public; Owner: voltov
--

COPY public.socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
3	ya29.A0AVA9y1ufb9Sibt1E8Wfo-vQCSsGHY357mLSXxfjHvl-waFeYJYGuak6VgjSBdavKYdQ6sxgi64Gif8c09W1P64Rovmurc3PA_8VpSAAet3ahmijnxciWAdzDOtOVR-SiEbmdjW_At4Ql-U3t1LqwWh1mit9vb68YUNnWUtBVEFTQVRBU0ZRRTY1ZHI4endpVms4ZlZ3eHlxVTNITUZPS1FJZw0166		2022-07-20 11:29:27.585088+00	3	1
\.


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 20, true);


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 68, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 21, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: core_about_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.core_about_id_seq', 1, true);


--
-- Name: core_maincategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.core_maincategory_id_seq', 3, true);


--
-- Name: core_mediaitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.core_mediaitem_id_seq', 25, true);


--
-- Name: core_mediaitem_likes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.core_mediaitem_likes_id_seq', 75, true);


--
-- Name: core_mediaitemreview_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.core_mediaitemreview_id_seq', 15, true);


--
-- Name: core_subcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.core_subcategory_id_seq', 3, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 124, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 17, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 45, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.socialaccount_socialaccount_id_seq', 3, true);


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_id_seq', 1, true);


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_sites_id_seq', 1, true);


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: voltov
--

SELECT pg_catalog.setval('public.socialaccount_socialtoken_id_seq', 3, true);


--
-- Name: account_emailaddress account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: core_about core_about_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_about
    ADD CONSTRAINT core_about_pkey PRIMARY KEY (id);


--
-- Name: core_maincategory core_maincategory_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_maincategory
    ADD CONSTRAINT core_maincategory_pkey PRIMARY KEY (id);


--
-- Name: core_maincategory core_maincategory_title_28ea58c2_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_maincategory
    ADD CONSTRAINT core_maincategory_title_28ea58c2_uniq UNIQUE (title);


--
-- Name: core_maincategory core_maincategory_title_en_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_maincategory
    ADD CONSTRAINT core_maincategory_title_en_key UNIQUE (title_en);


--
-- Name: core_maincategory core_maincategory_title_ru_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_maincategory
    ADD CONSTRAINT core_maincategory_title_ru_key UNIQUE (title_ru);


--
-- Name: core_mediaitem_likes core_mediaitem_likes_mediaitem_id_user_id_abb76088_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem_likes
    ADD CONSTRAINT core_mediaitem_likes_mediaitem_id_user_id_abb76088_uniq UNIQUE (mediaitem_id, user_id);


--
-- Name: core_mediaitem_likes core_mediaitem_likes_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem_likes
    ADD CONSTRAINT core_mediaitem_likes_pkey PRIMARY KEY (id);


--
-- Name: core_mediaitem core_mediaitem_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem
    ADD CONSTRAINT core_mediaitem_pkey PRIMARY KEY (id);


--
-- Name: core_mediaitem core_mediaitem_title_bb91c568_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem
    ADD CONSTRAINT core_mediaitem_title_bb91c568_uniq UNIQUE (title);


--
-- Name: core_mediaitem core_mediaitem_title_en_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem
    ADD CONSTRAINT core_mediaitem_title_en_key UNIQUE (title_en);


--
-- Name: core_mediaitem core_mediaitem_title_ru_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem
    ADD CONSTRAINT core_mediaitem_title_ru_key UNIQUE (title_ru);


--
-- Name: core_mediaitemreview core_mediaitemreview_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitemreview
    ADD CONSTRAINT core_mediaitemreview_pkey PRIMARY KEY (id);


--
-- Name: core_subcategory core_subcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_subcategory
    ADD CONSTRAINT core_subcategory_pkey PRIMARY KEY (id);


--
-- Name: core_subcategory core_subcategory_title_b4574e7f_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_subcategory
    ADD CONSTRAINT core_subcategory_title_b4574e7f_uniq UNIQUE (title);


--
-- Name: core_subcategory core_subcategory_title_en_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_subcategory
    ADD CONSTRAINT core_subcategory_title_en_key UNIQUE (title_en);


--
-- Name: core_subcategory core_subcategory_title_ru_key; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_subcategory
    ADD CONSTRAINT core_subcategory_title_ru_key UNIQUE (title_ru);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: core_maincategory_slug_a22ff210; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_maincategory_slug_a22ff210 ON public.core_maincategory USING btree (slug);


--
-- Name: core_maincategory_slug_a22ff210_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_maincategory_slug_a22ff210_like ON public.core_maincategory USING btree (slug varchar_pattern_ops);


--
-- Name: core_maincategory_title_28ea58c2_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_maincategory_title_28ea58c2_like ON public.core_maincategory USING btree (title varchar_pattern_ops);


--
-- Name: core_maincategory_title_en_7e26c28e_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_maincategory_title_en_7e26c28e_like ON public.core_maincategory USING btree (title_en varchar_pattern_ops);


--
-- Name: core_maincategory_title_ru_9a19c0d0_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_maincategory_title_ru_9a19c0d0_like ON public.core_maincategory USING btree (title_ru varchar_pattern_ops);


--
-- Name: core_mediaitem_likes_mediaitem_id_55d433e8; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_likes_mediaitem_id_55d433e8 ON public.core_mediaitem_likes USING btree (mediaitem_id);


--
-- Name: core_mediaitem_likes_user_id_d3e6993f; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_likes_user_id_d3e6993f ON public.core_mediaitem_likes USING btree (user_id);


--
-- Name: core_mediaitem_slug_41eb649a; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_slug_41eb649a ON public.core_mediaitem USING btree (slug);


--
-- Name: core_mediaitem_slug_41eb649a_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_slug_41eb649a_like ON public.core_mediaitem USING btree (slug varchar_pattern_ops);


--
-- Name: core_mediaitem_subcategory_id_bfbe9eb8; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_subcategory_id_bfbe9eb8 ON public.core_mediaitem USING btree (subcategory_id);


--
-- Name: core_mediaitem_title_bb91c568_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_title_bb91c568_like ON public.core_mediaitem USING btree (title varchar_pattern_ops);


--
-- Name: core_mediaitem_title_en_7eb888af_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_title_en_7eb888af_like ON public.core_mediaitem USING btree (title_en varchar_pattern_ops);


--
-- Name: core_mediaitem_title_ru_421376d6_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitem_title_ru_421376d6_like ON public.core_mediaitem USING btree (title_ru varchar_pattern_ops);


--
-- Name: core_mediaitemreview_media_item_id_d236d440; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitemreview_media_item_id_d236d440 ON public.core_mediaitemreview USING btree (media_item_id);


--
-- Name: core_mediaitemreview_user_id_471ad867; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_mediaitemreview_user_id_471ad867 ON public.core_mediaitemreview USING btree (user_id);


--
-- Name: core_subcategory_category_id_ca17dbdb; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_subcategory_category_id_ca17dbdb ON public.core_subcategory USING btree (category_id);


--
-- Name: core_subcategory_slug_10630aef; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_subcategory_slug_10630aef ON public.core_subcategory USING btree (slug);


--
-- Name: core_subcategory_slug_10630aef_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_subcategory_slug_10630aef_like ON public.core_subcategory USING btree (slug varchar_pattern_ops);


--
-- Name: core_subcategory_title_b4574e7f_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_subcategory_title_b4574e7f_like ON public.core_subcategory USING btree (title varchar_pattern_ops);


--
-- Name: core_subcategory_title_en_739df0c1_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_subcategory_title_en_739df0c1_like ON public.core_subcategory USING btree (title_en varchar_pattern_ops);


--
-- Name: core_subcategory_title_ru_89f22a04_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX core_subcategory_title_ru_89f22a04_like ON public.core_subcategory USING btree (title_ru varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: socialaccount_socialaccount_user_id_8146e70c; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON public.socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_site_id_2579dee5; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX socialaccount_socialapp_sites_site_id_2579dee5 ON public.socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_socialapp_id_97fb6e7d; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX socialaccount_socialapp_sites_socialapp_id_97fb6e7d ON public.socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_account_id_951f210e; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON public.socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_app_id_636a42d7; Type: INDEX; Schema: public; Owner: voltov
--

CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON public.socialaccount_socialtoken USING btree (app_id);


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_mediaitem_likes core_mediaitem_likes_mediaitem_id_55d433e8_fk_core_mediaitem_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem_likes
    ADD CONSTRAINT core_mediaitem_likes_mediaitem_id_55d433e8_fk_core_mediaitem_id FOREIGN KEY (mediaitem_id) REFERENCES public.core_mediaitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_mediaitem_likes core_mediaitem_likes_user_id_d3e6993f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem_likes
    ADD CONSTRAINT core_mediaitem_likes_user_id_d3e6993f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_mediaitem core_mediaitem_subcategory_id_bfbe9eb8_fk_core_subcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitem
    ADD CONSTRAINT core_mediaitem_subcategory_id_bfbe9eb8_fk_core_subcategory_id FOREIGN KEY (subcategory_id) REFERENCES public.core_subcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_mediaitemreview core_mediaitemreview_media_item_id_d236d440_fk_core_medi; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitemreview
    ADD CONSTRAINT core_mediaitemreview_media_item_id_d236d440_fk_core_medi FOREIGN KEY (media_item_id) REFERENCES public.core_mediaitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_mediaitemreview core_mediaitemreview_user_id_471ad867_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_mediaitemreview
    ADD CONSTRAINT core_mediaitemreview_user_id_471ad867_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_subcategory core_subcategory_category_id_ca17dbdb_fk_core_maincategory_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.core_subcategory
    ADD CONSTRAINT core_subcategory_category_id_ca17dbdb_fk_core_maincategory_id FOREIGN KEY (category_id) REFERENCES public.core_maincategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_site_id_2579dee5_fk_django_si; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc FOREIGN KEY (socialapp_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: voltov
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

