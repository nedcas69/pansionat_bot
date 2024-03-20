PGDMP     &                	    {            trades    15.3    15.3 &    "           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            #           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            $           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            %           1262    24788    trades    DATABASE     z   CREATE DATABASE trades WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE trades;
                postgres    false            �            1259    41315    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    41340    order    TABLE     @  CREATE TABLE public."order" (
    order_id integer NOT NULL,
    room_id integer,
    user_id bigint,
    fio character varying NOT NULL,
    tel character varying NOT NULL,
    room_number integer,
    room_class character varying,
    work boolean,
    date_start date,
    date_end date,
    tabel character varying,
    paytype character varying,
    pay_status boolean,
    sebe_35 integer,
    pension_30 integer,
    semye_70 integer,
    commerc_100 integer,
    summa integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);
    DROP TABLE public."order";
       public         heap    postgres    false            �            1259    41339    order_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.order_order_id_seq;
       public          postgres    false    220            &           0    0    order_order_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.order_order_id_seq OWNED BY public."order".order_id;
          public          postgres    false    219            �            1259    41330    role    TABLE     q   CREATE TABLE public.role (
    id integer NOT NULL,
    name character varying NOT NULL,
    permissions json
);
    DROP TABLE public.role;
       public         heap    postgres    false            �            1259    41329    role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.role_id_seq;
       public          postgres    false    218            '           0    0    role_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;
          public          postgres    false    217            �            1259    41321    room    TABLE     	  CREATE TABLE public.room (
    id integer NOT NULL,
    number character varying NOT NULL,
    number_of_seats integer NOT NULL,
    room_category character varying NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);
    DROP TABLE public.room;
       public         heap    postgres    false            �            1259    41320    room_id_seq    SEQUENCE     �   CREATE SEQUENCE public.room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.room_id_seq;
       public          postgres    false    216            (           0    0    room_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.room_id_seq OWNED BY public.room.id;
          public          postgres    false    215            �            1259    41354    user    TABLE     �  CREATE TABLE public."user" (
    id integer NOT NULL,
    email character varying,
    tabel character varying,
    tel character varying,
    fio character varying NOT NULL,
    registered_at timestamp without time zone,
    role_id integer,
    hashed_password character varying NOT NULL,
    work boolean,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    is_verified boolean NOT NULL
);
    DROP TABLE public."user";
       public         heap    postgres    false            �            1259    41353    user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.user_id_seq;
       public          postgres    false    222            )           0    0    user_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;
          public          postgres    false    221            z           2604    41343    order order_id    DEFAULT     r   ALTER TABLE ONLY public."order" ALTER COLUMN order_id SET DEFAULT nextval('public.order_order_id_seq'::regclass);
 ?   ALTER TABLE public."order" ALTER COLUMN order_id DROP DEFAULT;
       public          postgres    false    219    220    220            y           2604    41333    role id    DEFAULT     b   ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);
 6   ALTER TABLE public.role ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218            x           2604    41324    room id    DEFAULT     b   ALTER TABLE ONLY public.room ALTER COLUMN id SET DEFAULT nextval('public.room_id_seq'::regclass);
 6   ALTER TABLE public.room ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216            {           2604    41357    user id    DEFAULT     d   ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);
 8   ALTER TABLE public."user" ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    222    222                      0    41315    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    214   �*                 0    41340    order 
   TABLE DATA           �   COPY public."order" (order_id, room_id, user_id, fio, tel, room_number, room_class, work, date_start, date_end, tabel, paytype, pay_status, sebe_35, pension_30, semye_70, commerc_100, summa, created_at, updated_at) FROM stdin;
    public          postgres    false    220   +                 0    41330    role 
   TABLE DATA           5   COPY public.role (id, name, permissions) FROM stdin;
    public          postgres    false    218   $+                 0    41321    room 
   TABLE DATA           b   COPY public.room (id, number, number_of_seats, room_category, created_at, updated_at) FROM stdin;
    public          postgres    false    216   `+                 0    41354    user 
   TABLE DATA           �   COPY public."user" (id, email, tabel, tel, fio, registered_at, role_id, hashed_password, work, is_active, is_superuser, is_verified) FROM stdin;
    public          postgres    false    222   g/       *           0    0    order_order_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.order_order_id_seq', 43, true);
          public          postgres    false    219            +           0    0    role_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.role_id_seq', 1, false);
          public          postgres    false    217            ,           0    0    room_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.room_id_seq', 70, true);
          public          postgres    false    215            -           0    0    user_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.user_id_seq', 1, false);
          public          postgres    false    221            }           2606    41319 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    214            �           2606    41347    order order_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_pkey;
       public            postgres    false    220            �           2606    41337    role role_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.role DROP CONSTRAINT role_pkey;
       public            postgres    false    218                       2606    41328    room room_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.room DROP CONSTRAINT room_pkey;
       public            postgres    false    216            �           2606    41361    user user_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
       public            postgres    false    222            �           1259    41338 
   ix_role_id    INDEX     9   CREATE INDEX ix_role_id ON public.role USING btree (id);
    DROP INDEX public.ix_role_id;
       public            postgres    false    218            �           2606    41348    order order_room_id_fkey    FK CONSTRAINT     x   ALTER TABLE ONLY public."order"
    ADD CONSTRAINT order_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);
 D   ALTER TABLE ONLY public."order" DROP CONSTRAINT order_room_id_fkey;
       public          postgres    false    216    3199    220            �           2606    41362    user user_role_id_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);
 B   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_role_id_fkey;
       public          postgres    false    222    3202    218                  x�3154NN�0K11������ (��            x������ � �         ,   x�3�LL���㬎�SPP*.I,)-V�R()*M�ɫ����� ��
�         �  x���M�e5��׫`ſI��1e�3$��='O�+�T�B�T��:/�Ol��+_z����o�|���%U�K�_���|K�]�7i�D��(3n�"n�9A���֛[�*}Fdp��ǿ����g �\k.	"��8��f)�Y�%��b�����#9���I~?*�����I����	~%��zXn���ց�9�=��]�t��1dD�h��Z�cQZ�V9A��W��)��^4BƦ� �i����D�Nu��f	"��9˳�jE�]����Hp���Qt�s+t��ŭ�[�H:G��N�:Z�6�!	"�Z�4��l���nϺ��ġ���x/=�,쉐�ɯ������6����Hڥ�����E�v���9������ZG�[�D2��YGnx�m�H+t+�ϑ5�*�FHa�s#D,^�(��-;"��93��T��o�6��6z�� }��!���� ��!±�fA�~�y����Kw���WD��*e���a�[�Dڠ���f�u�6A�:Y���Ql&a;ςHt�f�b2E��"DV��U�o���uOC��.�Q�5�[�D&�e��slW�� 2�N�v_�%ږ��t���a�9m;mn����|Gd0s�v��X�9,�</�fNFG>K��"�!���
��v��gD3���͌).h/ҶF� r�Y2���:�G[�D3K�1�G�)A��'O7�1�z�m��r����#�Q�����t�,#X�\k�?o�"r�N����hCd<[ϊ����#����O�,�ж={����@������E0�7���jA�EƳ7��٨TT�j-��B'8�T��m+�`�$o]^{V���^"����A0�n�ZԷ{-�B��2����!곅-� �eGgi���7��C'ˎ��T�j�	D�q������:��,���#��Q�����"����][a�h	�W�o��ᣅmkƊ�U�$�T��p��}Ӯ�~.D�7��	�            x������ � �     