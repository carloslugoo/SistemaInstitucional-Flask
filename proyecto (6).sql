-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 11-01-2023 a las 23:15:16
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admin`
--

CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL,
  `nmb_ad` varchar(40) NOT NULL,
  `ape_ad` varchar(40) NOT NULL,
  `ci_ad` int(10) NOT NULL,
  `tel_ad` int(14) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `tipo_u` int(1) NOT NULL DEFAULT 3,
  `edad` int(2) NOT NULL,
  `email` varchar(45) NOT NULL,
  `loc_ad` varchar(65) NOT NULL,
  `fec_ad` date DEFAULT NULL,
  `bar_ad` varchar(45) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `admin`
--

INSERT INTO `admin` (`id_admin`, `nmb_ad`, `ape_ad`, `ci_ad`, `tel_ad`, `id_user`, `tipo_u`, `edad`, `email`, `loc_ad`, `fec_ad`, `bar_ad`, `estado`) VALUES
(1, 'Lourdes Rosalia', 'Zacarias', 2064125, 985110362, 20, 3, 42, 'testadmin@gmail.com', 'Encarnación', NULL, 'Cuidad Nueva', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `id_alumno` int(11) NOT NULL,
  `nmb_a` varchar(45) NOT NULL,
  `ape_a` varchar(45) NOT NULL,
  `tel_a` int(10) DEFAULT NULL,
  `id_curso` int(11) NOT NULL,
  `ci_a` int(10) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `tipo_u` int(1) NOT NULL DEFAULT 1,
  `edad` int(2) NOT NULL,
  `email` varchar(45) NOT NULL,
  `loc_a` varchar(80) NOT NULL,
  `nmb_tu` varchar(45) NOT NULL,
  `tel_tu` int(14) NOT NULL,
  `fec_a` date DEFAULT NULL,
  `bar_a` varchar(45) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`id_alumno`, `nmb_a`, `ape_a`, `tel_a`, `id_curso`, `ci_a`, `id_user`, `tipo_u`, `edad`, `email`, `loc_a`, `nmb_tu`, `tel_tu`, `fec_a`, `bar_a`, `estado`) VALUES
(64, 'Carlos Gabriel', 'Lugo Zacarias', 985475222, 1, 4922377, 17, 1, 19, 'ostias@gmail.com', 'Encarnación', 'Lourdes Z', 985110325, '2001-12-31', 'Cuidad Nueva', 1),
(65, 'Mathias ', 'Ortellado Silva', 985114432, 1, 4851123, NULL, 1, 16, 'test@g.com', 'Encarnación', 'Osvlado', 985110325, '2001-12-31', 'Cuidad Nueva', 1),
(66, 'Carlos Abel', 'Lugo Z', 985114432, 1, 4922378, NULL, 1, 19, 'ostias@gmail.com', 'Encarnación', 'Lourdes Z', 984752321, '2001-12-31', 'Cuidad Nueva', 1),
(67, 'Carlos', 'Ibarra', 985115555, 1, 3452348, NULL, 1, 22, 'ibarra@gmail.com', 'Encarnación', 'Ibarra City', 985888887, '2000-10-21', 'Ni idea', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistenciaalum`
--

CREATE TABLE `asistenciaalum` (
  `id_asisalum` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `asistio` varchar(1) NOT NULL,
  `id_curso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `asistenciaalum`
--

INSERT INTO `asistenciaalum` (`id_asisalum`, `id_alumno`, `id_materia`, `fecha`, `asistio`, `id_curso`) VALUES
(11, 66, 20, '2023-01-05', 'P', 1),
(12, 64, 20, '2023-01-05', 'P', 1),
(13, 65, 20, '2023-01-05', 'P', 1),
(14, 66, 20, '2023-01-06', 'A', 1),
(15, 64, 20, '2023-01-06', 'P', 1),
(16, 65, 20, '2023-01-06', 'A', 1),
(17, 66, 20, '2023-01-04', 'A', 1),
(18, 64, 20, '2023-01-04', 'A', 1),
(19, 65, 20, '2023-01-04', 'P', 1),
(20, 66, 20, '2023-01-07', 'A', 1),
(21, 64, 20, '2023-01-07', 'P', 1),
(22, 65, 20, '2023-01-07', 'P', 1),
(23, 66, 20, '2023-01-09', 'P', 1),
(24, 64, 20, '2023-01-09', 'A', 1),
(25, 65, 20, '2023-01-09', 'P', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistenciaprof`
--

CREATE TABLE `asistenciaprof` (
  `id_asisprof` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `fec_a` date NOT NULL,
  `hora_e` time DEFAULT NULL,
  `hora_s` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `asistenciaprof`
--

INSERT INTO `asistenciaprof` (`id_asisprof`, `id_profesor`, `fec_a`, `hora_e`, `hora_s`) VALUES
(40, 1, '2023-01-02', '22:41:36', NULL),
(41, 51, '2023-01-02', NULL, NULL),
(45, 1, '2023-01-03', '04:00:11', '04:00:15'),
(46, 51, '2023-01-03', NULL, NULL),
(47, 1, '2023-01-03', '04:00:11', '04:00:15'),
(48, 1, '2023-01-02', '22:41:36', NULL),
(49, 1, '2023-01-03', '04:00:11', '04:00:15'),
(50, 1, '2023-01-03', '04:00:11', '04:00:15'),
(51, 1, '2023-01-02', '22:41:36', NULL),
(52, 1, '2023-01-03', '04:00:11', '04:00:15'),
(53, 1, '2023-01-02', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuotas`
--

CREATE TABLE `cuotas` (
  `id_cuota` int(11) NOT NULL,
  `estado` int(1) NOT NULL,
  `fecha` date NOT NULL,
  `id_tipoc` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id_curso` int(11) NOT NULL,
  `des_c` varchar(40) NOT NULL,
  `sec_c` varchar(5) NOT NULL,
  `id_enfasis` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`id_curso`, `des_c`, `sec_c`, `id_enfasis`) VALUES
(1, 'Primer Curso', 'A', 1),
(2, 'Segundo Curso', 'A', 1),
(3, 'Primer Curso', 'A', 2),
(4, 'Tercer Curso', 'A', 1),
(5, 'Segundo Curso', 'A', 2),
(6, 'Tercer Curso', 'A', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dias`
--

CREATE TABLE `dias` (
  `id_dia` int(11) NOT NULL,
  `des_d` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `dias`
--

INSERT INTO `dias` (`id_dia`, `des_d`) VALUES
(1, 'Lunes'),
(2, 'Martes'),
(3, 'Miercoles'),
(4, 'Jueves'),
(5, 'Viernes'),
(6, 'Sabado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `enfasis`
--

CREATE TABLE `enfasis` (
  `id_enfasis` int(11) NOT NULL,
  `des_e` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `enfasis`
--

INSERT INTO `enfasis` (`id_enfasis`, `des_e`) VALUES
(1, 'Contabilidad'),
(2, 'Sociales');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios`
--

CREATE TABLE `horarios` (
  `id_horario` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `id_dia` int(11) NOT NULL,
  `hora_i` time NOT NULL,
  `hora_f` time NOT NULL,
  `id_profesor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `horarios`
--

INSERT INTO `horarios` (`id_horario`, `id_curso`, `id_materia`, `id_dia`, `hora_i`, `hora_f`, `id_profesor`) VALUES
(179, 1, 20, 1, '17:00:00', '17:40:00', 1),
(180, 1, 20, 1, '17:40:00', '18:20:00', 1),
(181, 1, 35, 1, '18:20:00', '19:00:00', 0),
(182, 1, 35, 1, '19:00:00', '19:40:00', 0),
(183, 1, 20, 1, '20:20:00', '21:00:00', 1),
(184, 1, 27, 1, '21:00:00', '21:40:00', 0),
(185, 1, 27, 1, '21:40:00', '22:20:00', 0),
(186, 1, 18, 2, '17:00:00', '17:40:00', 0),
(187, 1, 18, 2, '17:40:00', '18:20:00', 0),
(188, 1, 18, 2, '18:20:00', '19:00:00', 0),
(189, 1, 18, 2, '19:00:00', '19:40:00', 0),
(190, 1, 20, 2, '20:20:00', '21:00:00', 1),
(191, 1, 20, 2, '21:00:00', '21:40:00', 1),
(192, 1, 31, 2, '21:40:00', '22:20:00', 52),
(193, 1, 20, 3, '17:00:00', '17:40:00', 1),
(194, 1, 29, 3, '17:40:00', '18:20:00', 51),
(195, 1, 29, 3, '18:20:00', '19:00:00', 51),
(196, 1, 29, 3, '19:00:00', '19:40:00', 51),
(197, 1, 27, 3, '20:20:00', '21:00:00', 0),
(198, 1, 27, 3, '21:00:00', '21:40:00', 0),
(199, 1, 20, 3, '21:40:00', '22:20:00', 1),
(200, 1, 19, 4, '17:00:00', '17:40:00', 0),
(201, 1, 35, 4, '17:40:00', '18:20:00', 0),
(202, 1, 25, 4, '18:20:00', '19:00:00', 55),
(203, 1, 31, 4, '19:00:00', '19:40:00', 52),
(204, 1, 31, 4, '20:20:00', '21:00:00', 52),
(205, 1, 16, 4, '21:00:00', '21:40:00', 50),
(206, 1, 16, 4, '21:40:00', '22:20:00', 50),
(207, 1, 29, 5, '17:00:00', '17:40:00', 51),
(208, 1, 18, 5, '17:40:00', '18:20:00', 0),
(209, 1, 18, 5, '18:20:00', '19:00:00', 0),
(210, 1, 27, 5, '19:00:00', '19:40:00', 0),
(211, 1, 27, 5, '20:20:00', '21:00:00', 0),
(212, 1, 27, 5, '21:00:00', '21:40:00', 0),
(213, 1, 27, 5, '21:40:00', '22:20:00', 0),
(214, 1, 18, 6, '13:00:00', '13:40:00', 0),
(215, 1, 18, 6, '13:40:00', '14:20:00', 0),
(216, 1, 18, 6, '14:20:00', '15:00:00', 0),
(217, 1, 34, 6, '15:00:00', '15:40:00', 0),
(218, 1, 27, 6, '16:20:00', '17:00:00', 0),
(219, 1, 34, 6, '17:00:00', '17:40:00', 0),
(220, 1, 20, 6, '17:40:00', '18:20:00', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `indicadores`
--

CREATE TABLE `indicadores` (
  `id_indicador` int(11) NOT NULL,
  `des_i` varchar(50) NOT NULL,
  `pun_i` int(3) NOT NULL,
  `id_trabajo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `indicadores`
--

INSERT INTO `indicadores` (`id_indicador`, `des_i`, `pun_i`, `id_trabajo`) VALUES
(174, 'Entrega en Fecha', 2, 104),
(175, 'Esucha tus compas', 2, 104),
(176, 'Completa totalmente', 2, 104),
(177, 'Pulcritud', 2, 104),
(178, 'Creatividad', 2, 104),
(179, 'Entrega en Fecha', 2, 105),
(180, 'Cumple los requisitos ', 2, 105),
(181, 'Identifica todo los identifica', 2, 105),
(182, 'Creatividad', 2, 105),
(183, 'Otro indicador', 2, 105),
(184, 'Identifica los químicos ', 2, 106),
(185, 'Completas los espacios ', 2, 106),
(186, 'Reflexiona sobre los temas', 2, 106),
(187, 'Completa las preguntas', 2, 106),
(188, 'Verdadero o Falso', 2, 106),
(189, 'Entrega en Fecha', 2, 107),
(190, 'Cumple los requisitos', 2, 107),
(191, 'Perseverancia y xd', 2, 107),
(192, 'Pulcritud', 2, 107),
(193, 'Creatividad', 2, 107),
(194, 'Entrega en Fecha', 1, 108),
(195, 'A', 1, 108),
(196, 'B', 1, 108),
(197, 'Creatividad', 1, 108),
(198, 'Creatividad', 1, 108),
(199, 'Entrega en Fecha', 2, 109),
(200, 'A', 2, 109),
(201, 'B', 2, 109),
(202, 'C', 2, 109),
(203, 'D', 2, 109),
(204, 'Entrega en Fecha', 2, 112),
(205, 'A', 1, 112),
(206, 'B', 2, 112),
(207, 'Entrega en Fecha', 2, 113),
(208, 'Esucha tus compas', 2, 113),
(209, 'Perseverancia y xd', 2, 113);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `indxalum`
--

CREATE TABLE `indxalum` (
  `id_ixa` int(11) NOT NULL,
  `id_indicador` int(11) NOT NULL,
  `id_trabajo` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL,
  `pun_l` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `indxalum`
--

INSERT INTO `indxalum` (`id_ixa`, `id_indicador`, `id_trabajo`, `id_alumno`, `pun_l`) VALUES
(193, 174, 104, 66, 2),
(194, 175, 104, 66, 2),
(195, 176, 104, 66, 2),
(196, 177, 104, 66, 2),
(197, 178, 104, 66, 2),
(198, 174, 104, 64, 0),
(199, 175, 104, 64, 0),
(200, 176, 104, 64, 2),
(201, 177, 104, 64, 0),
(202, 178, 104, 64, 0),
(203, 174, 104, 65, 2),
(204, 175, 104, 65, 0),
(205, 176, 104, 65, 2),
(206, 177, 104, 65, 0),
(207, 178, 104, 65, 2),
(208, 179, 105, 66, 2),
(209, 180, 105, 66, 0),
(210, 181, 105, 66, 2),
(211, 182, 105, 66, 2),
(212, 183, 105, 66, 2),
(213, 179, 105, 64, 2),
(214, 180, 105, 64, 2),
(215, 181, 105, 64, 0),
(216, 182, 105, 64, 0),
(217, 183, 105, 64, 0),
(218, 179, 105, 65, 2),
(219, 180, 105, 65, 2),
(220, 181, 105, 65, 2),
(221, 182, 105, 65, 2),
(222, 183, 105, 65, 2),
(297, 204, 112, 66, 2),
(298, 205, 112, 66, 1),
(299, 206, 112, 66, 2),
(300, 204, 112, 64, 2),
(301, 205, 112, 64, 1),
(302, 206, 112, 64, 0),
(303, 204, 112, 65, 2),
(304, 205, 112, 65, 0),
(305, 206, 112, 65, 0),
(306, 207, 113, 66, 2),
(307, 208, 113, 66, 2),
(308, 209, 113, 66, 2),
(309, 207, 113, 64, 2),
(310, 208, 113, 64, 2),
(311, 209, 113, 64, 2),
(312, 207, 113, 65, 2),
(313, 208, 113, 65, 2),
(314, 209, 113, 65, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `log`
--

CREATE TABLE `log` (
  `id_log` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `accion` varchar(45) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id_materia` int(11) NOT NULL,
  `des_m` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`id_materia`, `des_m`) VALUES
(14, 'Lengua Castellana y Literatura'),
(15, 'Guaraní Ñe\'ẽ '),
(16, 'Lengua Extranjera'),
(18, 'Ciencias Naturales y Salud'),
(19, 'Física'),
(20, 'Química '),
(22, 'Matemática '),
(24, 'Historia y Geografía '),
(25, 'Formación Ética y Ciudadana'),
(26, 'Psicología '),
(27, 'Sociología y Antropología Cultural'),
(29, 'Educación Física'),
(31, 'Orientación Educacional y Socio Laboral'),
(33, 'Contabilidad y Legislación'),
(34, 'Seminario Contable '),
(35, 'Cálculo Mercantil y Financiero'),
(36, 'Administración de Empresas'),
(37, 'Informática '),
(38, 'Introducción a la Economía'),
(39, 'Legislación Tributaria '),
(40, 'Código Laboral'),
(41, 'Economía y Gestión'),
(42, 'Filosofía'),
(43, 'Antropología Social'),
(44, 'Artes'),
(45, 'Política '),
(46, 'Antropología Cultural'),
(47, 'Sociología '),
(48, 'Investigación Social'),
(49, 'Estadística'),
(50, 'Educación Económica y Financiera'),
(51, 'Educación para la Seguridad Vial'),
(52, 'Metodología de la Investigación');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matxalum`
--

CREATE TABLE `matxalum` (
  `id_mxa` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `cal` int(1) DEFAULT NULL,
  `id_curso` int(2) NOT NULL,
  `pun_ac` int(3) NOT NULL,
  `ano_m` int(4) NOT NULL,
  `id_profesor` int(2) DEFAULT NULL,
  `cal2` int(11) DEFAULT NULL,
  `pun_ac2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `matxalum`
--

INSERT INTO `matxalum` (`id_mxa`, `id_alumno`, `id_materia`, `cal`, `id_curso`, `pun_ac`, `ano_m`, `id_profesor`, `cal2`, `pun_ac2`) VALUES
(345, 64, 14, NULL, 1, 0, 2022, 1, NULL, 0),
(346, 64, 15, NULL, 1, 0, 2022, 1, NULL, 0),
(347, 64, 16, NULL, 1, 0, 2022, 0, NULL, 0),
(348, 64, 18, NULL, 1, 0, 2022, 0, NULL, 0),
(349, 64, 19, NULL, 1, 0, 2022, 0, NULL, 0),
(350, 64, 20, NULL, 1, 19, 2022, 1, NULL, 6),
(351, 64, 22, NULL, 1, 0, 2022, 0, NULL, 0),
(352, 64, 24, NULL, 1, 0, 2022, 0, NULL, 0),
(353, 64, 25, NULL, 1, 0, 2022, 0, NULL, 0),
(354, 64, 27, NULL, 1, 0, 2022, 0, NULL, 0),
(355, 64, 29, NULL, 1, 0, 2022, 0, NULL, 0),
(356, 64, 31, NULL, 1, 0, 2022, 0, NULL, 0),
(357, 64, 33, NULL, 1, 0, 2022, 0, NULL, 0),
(358, 64, 34, NULL, 1, 0, 2022, 0, NULL, 0),
(359, 64, 35, NULL, 1, 0, 2022, 0, NULL, 0),
(360, 64, 37, NULL, 1, 0, 2022, 0, NULL, 0),
(361, 65, 14, NULL, 1, 0, 2022, 1, NULL, 0),
(362, 65, 15, NULL, 1, 0, 2022, 1, NULL, 0),
(363, 65, 16, NULL, 1, 0, 2022, 0, NULL, 0),
(364, 65, 18, NULL, 1, 0, 2022, 0, NULL, 0),
(365, 65, 19, NULL, 1, 0, 2022, 0, NULL, 0),
(366, 65, 20, NULL, 1, 8, 2022, 1, NULL, 6),
(367, 65, 22, NULL, 1, 0, 2022, 0, NULL, 0),
(368, 65, 24, NULL, 1, 0, 2022, 0, NULL, 0),
(369, 65, 25, NULL, 1, 0, 2022, 0, NULL, 0),
(370, 65, 27, NULL, 1, 0, 2022, 0, NULL, 0),
(371, 65, 29, NULL, 1, 0, 2022, 0, NULL, 0),
(372, 65, 31, NULL, 1, 0, 2022, 0, NULL, 0),
(373, 65, 33, NULL, 1, 0, 2022, 0, NULL, 0),
(374, 65, 34, NULL, 1, 0, 2022, 0, NULL, 0),
(375, 65, 35, NULL, 1, 0, 2022, 0, NULL, 0),
(376, 65, 37, NULL, 1, 0, 2022, 0, NULL, 0),
(377, 66, 14, NULL, 1, 0, 2022, 1, NULL, 0),
(378, 66, 15, NULL, 1, 0, 2022, 1, NULL, 0),
(379, 66, 16, NULL, 1, 0, 2022, 0, NULL, 0),
(380, 66, 18, NULL, 1, 0, 2022, 0, NULL, 0),
(381, 66, 19, NULL, 1, 0, 2022, 0, NULL, 0),
(382, 66, 20, NULL, 1, 23, 2022, 1, NULL, 6),
(383, 66, 22, NULL, 1, 0, 2022, 0, NULL, 0),
(384, 66, 24, NULL, 1, 0, 2022, 0, NULL, 0),
(385, 66, 25, NULL, 1, 0, 2022, 0, NULL, 0),
(386, 66, 27, NULL, 1, 0, 2022, 0, NULL, 0),
(387, 66, 29, NULL, 1, 0, 2022, 0, NULL, 0),
(388, 66, 31, NULL, 1, 0, 2022, 0, NULL, 0),
(389, 66, 33, NULL, 1, 0, 2022, 0, NULL, 0),
(390, 66, 34, NULL, 1, 0, 2022, 0, NULL, 0),
(391, 66, 35, NULL, 1, 0, 2022, 0, NULL, 0),
(392, 66, 37, NULL, 1, 0, 2022, 0, NULL, 0),
(393, 67, 16, NULL, 1, 0, 2022, 0, NULL, 0),
(394, 67, 22, NULL, 1, 0, 2022, 0, NULL, 0),
(395, 67, 24, NULL, 1, 0, 2022, 0, NULL, 0),
(396, 67, 25, NULL, 1, 0, 2022, 0, NULL, 0),
(397, 67, 27, NULL, 1, 0, 2022, 0, NULL, 0),
(398, 67, 29, NULL, 1, 0, 2022, 0, NULL, 0),
(399, 67, 31, NULL, 1, 0, 2022, 0, NULL, 0),
(400, 67, 37, NULL, 1, 0, 2022, 0, NULL, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matxcur`
--

CREATE TABLE `matxcur` (
  `id_matxcur` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `id_enfasis` int(11) NOT NULL,
  `car_h` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `matxcur`
--

INSERT INTO `matxcur` (`id_matxcur`, `id_curso`, `id_materia`, `id_enfasis`, `car_h`) VALUES
(4, 1, 14, 1, 5),
(5, 2, 14, 1, 5),
(6, 4, 14, 1, 4),
(7, 1, 15, 1, 2),
(8, 2, 15, 1, 4),
(9, 1, 16, 1, 2),
(10, 2, 16, 1, 4),
(14, 1, 18, 1, 2),
(15, 2, 18, 1, 2),
(16, 4, 18, 1, 2),
(17, 1, 19, 1, 2),
(18, 2, 19, 1, 4),
(19, 1, 20, 1, 2),
(20, 2, 20, 1, 4),
(24, 1, 22, 1, 3),
(25, 2, 22, 1, 3),
(26, 4, 22, 1, 3),
(30, 1, 24, 1, 2),
(31, 2, 24, 1, 2),
(32, 4, 24, 1, 2),
(33, 1, 25, 1, 2),
(34, 2, 51, 1, 2),
(35, 4, 26, 1, 4),
(36, 1, 27, 1, 2),
(40, 1, 29, 1, 2),
(41, 2, 29, 1, 2),
(42, 4, 29, 1, 2),
(45, 1, 31, 1, 2),
(46, 4, 31, 1, 2),
(50, 1, 33, 1, 6),
(51, 2, 33, 1, 6),
(52, 4, 33, 1, 6),
(53, 1, 34, 1, 6),
(54, 2, 34, 1, 6),
(55, 4, 34, 1, 6),
(56, 1, 35, 1, 4),
(57, 2, 35, 1, 4),
(58, 4, 35, 1, 4),
(59, 2, 36, 1, 3),
(60, 4, 36, 1, 3),
(61, 1, 37, 1, 2),
(62, 2, 37, 1, 2),
(63, 4, 37, 1, 3),
(64, 4, 38, 1, 3),
(65, 4, 39, 1, 3),
(66, 4, 40, 1, 3),
(67, 3, 14, 2, 3),
(68, 5, 14, 2, 4),
(69, 6, 14, 2, 5),
(70, 3, 15, 2, 2),
(71, 5, 15, 2, 2),
(72, 6, 15, 2, 2),
(73, 3, 16, 2, 2),
(74, 5, 16, 2, 2),
(75, 6, 16, 2, 3),
(76, 3, 18, 2, 3),
(77, 5, 18, 2, 4),
(78, 5, 19, 2, 4),
(79, 6, 19, 2, 4),
(80, 5, 20, 2, 4),
(81, 6, 20, 2, 4),
(82, 3, 22, 2, 5),
(83, 5, 22, 2, 4),
(84, 6, 22, 2, 3),
(85, 3, 24, 2, 2),
(86, 5, 24, 2, 2),
(87, 6, 24, 2, 2),
(88, 5, 25, 2, 2),
(89, 3, 26, 2, 4),
(90, 6, 41, 2, 2),
(91, 5, 42, 2, 2),
(92, 3, 43, 2, 2),
(93, 3, 29, 2, 2),
(94, 5, 29, 2, 2),
(95, 6, 29, 2, 2),
(96, 3, 44, 2, 4),
(97, 5, 44, 2, 2),
(98, 5, 31, 2, 4),
(99, 6, 31, 2, 2),
(100, 6, 45, 2, 2),
(101, 3, 46, 2, 4),
(102, 6, 47, 2, 3),
(103, 5, 48, 2, 2),
(104, 3, 49, 2, 2),
(105, 6, 50, 2, 3),
(106, 3, 51, 2, 4),
(107, 6, 52, 2, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matxpro`
--

CREATE TABLE `matxpro` (
  `id_mxp` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  `fecha` int(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `matxpro`
--

INSERT INTO `matxpro` (`id_mxp`, `id_materia`, `id_profesor`, `id_curso`, `fecha`) VALUES
(46, 16, 50, 1, 2022),
(47, 16, 50, 2, 2022),
(48, 29, 51, 3, 2022),
(49, 29, 51, 5, 2022),
(50, 31, 51, 5, 2022),
(51, 29, 51, 6, 2022),
(52, 52, 51, 6, 2022),
(53, 29, 51, 1, 2022),
(54, 15, 52, 3, 2022),
(55, 26, 52, 3, 2022),
(56, 46, 52, 3, 2022),
(57, 15, 52, 6, 2022),
(58, 31, 52, 6, 2022),
(59, 31, 52, 1, 2022),
(60, 14, 54, 6, 2022),
(61, 38, 54, 4, 2022),
(62, 43, 55, 3, 2022),
(63, 24, 0, 1, 2022),
(64, 25, 55, 1, 2022),
(65, 24, 55, 2, 2022),
(66, 24, 55, 4, 2022),
(67, 37, 56, 1, 2022),
(68, 37, 56, 2, 2022),
(69, 37, 56, 4, 2022),
(70, 19, 57, 2, 2022),
(71, 49, 58, 3, 2022),
(72, 20, 58, 6, 2022),
(73, 15, 58, 1, 2022),
(74, 20, 58, 2, 2022),
(75, 24, 59, 3, 2022),
(76, 24, 59, 5, 2022),
(77, 25, 59, 5, 2022),
(78, 40, 0, 4, 2022),
(79, 14, 0, 1, 2022),
(80, 51, 0, 2, 2022),
(81, 29, 0, 2, 2022),
(82, 29, 0, 4, 2022),
(83, 39, 0, 4, 2022),
(84, 18, 0, 1, 2022),
(85, 48, 0, 5, 2022),
(86, 20, 1, 1, 2022);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planillas`
--

CREATE TABLE `planillas` (
  `id_planillas` int(11) NOT NULL,
  `filename` varchar(50) NOT NULL,
  `estado` int(1) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `fecha_m` date NOT NULL,
  `fecha_r` date DEFAULT NULL,
  `des_p` varchar(70) DEFAULT NULL,
  `cp` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `planillas`
--

INSERT INTO `planillas` (`id_planillas`, `filename`, `estado`, `id_profesor`, `fecha_m`, `fecha_r`, `des_p`, `cp`) VALUES
(1, 'planillapendiente_11.xls', 1, 1, '2023-01-09', '2023-01-09', 'Planilla de Proceso de Tercer Curso Sociales A TM', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `id_profesor` int(11) NOT NULL,
  `nmb_p` varchar(40) NOT NULL,
  `ape_p` varchar(40) NOT NULL,
  `tel_p` varchar(40) NOT NULL,
  `ci_p` int(10) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `tipo_u` int(1) NOT NULL DEFAULT 2,
  `edad` int(2) NOT NULL,
  `email` varchar(45) NOT NULL,
  `loc_p` varchar(80) NOT NULL,
  `fec_p` date DEFAULT NULL,
  `bar_p` varchar(45) NOT NULL,
  `estado` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`id_profesor`, `nmb_p`, `ape_p`, `tel_p`, `ci_p`, `id_user`, `tipo_u`, `edad`, `email`, `loc_p`, `fec_p`, `bar_p`, `estado`) VALUES
(1, 'Carlos Gabriel', 'Lugo Z', '0985114432', 4851123, 18, 2, 50, 'ostias@gmail.com', 'Encarnación', '2001-12-31', 'Cuidad Nueva', 1),
(50, 'María Bárbara Edith', 'Cañete de Ayala', '0985260798', 2255639, NULL, 2, 46, 'mabaedcb@hotmail.com', 'Encarnación', '1975-12-04', 'San Padre Casco Antiguo', 1),
(51, 'Carolina Antonia', 'Meza Gauto', '0972630069', 2921970, NULL, 2, 42, 'carolina.meza@gmail.com', 'Encarnación', '1980-01-03', 'Padre Kreuser 781', 1),
(52, 'Liliana Andrea', 'Giménez Congregado', '0985778757', 2594667, NULL, 2, 41, 'liandygi@hotmail.com', 'Encarnación', '1981-04-07', 'Quiteria ', 1),
(53, 'Mirta Graciela', ' González Maidana', '0985789126', 2343686, NULL, 2, 4, 'grachel.gonzalez@gmail.com', 'Encarnación', '1977-08-28', 'Primera Proyectada', 1),
(54, 'Sirley Marlene', 'Maciel del Puerto', '0983582774', 3559827, NULL, 2, 38, 'shirleymaciel4@gmail.com', 'Encarnación', '1983-11-17', 'Centro', 1),
(55, 'Lourdes Rosalia', 'Zacarias Benítez ', '0985110362', 2064125, NULL, 2, 47, 'lourdeszaca@gmail.com', 'Encarnación', '1975-11-11', 'Cuidad Nueva', 1),
(56, 'Aureliano Emanuel', 'González Medina', '0992309763', 4028364, NULL, 2, 35, 'aurelianoegonzalezm@gmail.com', 'Encarnación', '1987-06-22', 'Pacu Cua', 1),
(57, 'Nelsy Natalia', 'Salinas Gonzáles ', '0984510313', 1534917, NULL, 2, 41, 'neslynatal@hotmail.com', 'Encarnación', '1981-06-02', 'Ciudad Nueva', 1),
(58, 'Lelio Enrique', 'Martínez Pereira', '0985760508', 1624277, NULL, 2, 54, 'lelio@gmail.com', 'Encarnación', '1968-05-20', 'Pacu Cua', 1),
(59, 'Mirian Susana', 'Leiva de Gómez de la Fuente', '0985341026', 2983679, NULL, 2, 42, 'su_323@hotmail.es', 'Encarnación', '1980-07-21', 'Conavi', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_user`
--

CREATE TABLE `tipo_user` (
  `tipo_u` int(11) NOT NULL,
  `des_u` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tipo_user`
--

INSERT INTO `tipo_user` (`tipo_u`, `des_u`) VALUES
(1, 'Alumnos'),
(2, 'Docentes'),
(3, 'Admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajos`
--

CREATE TABLE `trabajos` (
  `id_trabajo` int(11) NOT NULL,
  `fec_t` date NOT NULL,
  `des_t` varchar(45) NOT NULL,
  `pun_t` int(3) NOT NULL,
  `id_profesor` int(11) NOT NULL,
  `id_materia` int(11) NOT NULL,
  `tipo_t` varchar(40) NOT NULL,
  `clave_t` varchar(5) NOT NULL,
  `id_curso` int(1) NOT NULL,
  `etapa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `trabajos`
--

INSERT INTO `trabajos` (`id_trabajo`, `fec_t`, `des_t`, `pun_t`, `id_profesor`, `id_materia`, `tipo_t`, `clave_t`, `id_curso`, `etapa`) VALUES
(104, '2022-12-23', 'Célula ', 10, 1, 20, 'tra_pro', 'BmW2F', 1, 1),
(105, '2022-12-23', 'Metamorfosis ', 10, 1, 20, 'tra_pru', 'j6NiX', 1, 1),
(112, '2023-01-03', 'Animales', 5, 1, 20, 'tra_pru', 'VRLGB', 1, 1),
(113, '2023-01-03', 'Quimicos Historicos', 6, 1, 20, 'tra_pru', 'p66nj', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `traxalum`
--

CREATE TABLE `traxalum` (
  `id_txa` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL,
  `pun_l` int(11) NOT NULL,
  `fec_t` int(11) NOT NULL,
  `id_trabajo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `traxalum`
--

INSERT INTO `traxalum` (`id_txa`, `id_alumno`, `pun_l`, `fec_t`, `id_trabajo`) VALUES
(91, 66, 10, 2022, 104),
(92, 64, 2, 2022, 104),
(93, 65, 6, 2022, 104),
(94, 66, 8, 2022, 105),
(95, 64, 4, 2022, 105),
(96, 65, 10, 2022, 105),
(109, 66, 5, 2023, 112),
(110, 64, 3, 2023, 112),
(111, 65, 2, 2023, 112),
(112, 66, 6, 2023, 113),
(113, 64, 6, 2023, 113),
(114, 65, 6, 2023, 113);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `email` varchar(20) NOT NULL,
  `password` longtext NOT NULL,
  `tipo_u` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id_user`, `username`, `email`, `password`, `tipo_u`) VALUES
(17, 'test', 'gabi2@gmail.com', 'pbkdf2:sha256:260000$qY1O7ZojmqtmS1R0$d9a3fd94fef2bfe23b8342331099d61f5086f851c29806e5a8952738aa1a4a15', 1),
(18, 'test2', 'test@g.com', 'pbkdf2:sha256:260000$E7uzqti18jPlft63$1294b31cef6d0a22a162baca8d22598026efc5a3f89a7b5c0c8470cd8598e512', 2),
(19, 'test2', 'test@g.com', 'pbkdf2:sha256:260000$Poa1e9Wv26t9664S$0ffc5fcd935df168350b69aab4aa594cea581ad5670d6ca336c73ae785ea67ab', 2),
(20, 'test3', 'test@g.com', 'pbkdf2:sha256:260000$jc4sgZrkMajOWzRF$b63c2052bee536c6f02055f4c29208a807ed0624247d635e9d82436b68fd1c68', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`);

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`id_alumno`);

--
-- Indices de la tabla `asistenciaalum`
--
ALTER TABLE `asistenciaalum`
  ADD PRIMARY KEY (`id_asisalum`);

--
-- Indices de la tabla `asistenciaprof`
--
ALTER TABLE `asistenciaprof`
  ADD PRIMARY KEY (`id_asisprof`);

--
-- Indices de la tabla `cuotas`
--
ALTER TABLE `cuotas`
  ADD PRIMARY KEY (`id_cuota`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id_curso`);

--
-- Indices de la tabla `dias`
--
ALTER TABLE `dias`
  ADD PRIMARY KEY (`id_dia`);

--
-- Indices de la tabla `enfasis`
--
ALTER TABLE `enfasis`
  ADD PRIMARY KEY (`id_enfasis`);

--
-- Indices de la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD PRIMARY KEY (`id_horario`);

--
-- Indices de la tabla `indicadores`
--
ALTER TABLE `indicadores`
  ADD PRIMARY KEY (`id_indicador`);

--
-- Indices de la tabla `indxalum`
--
ALTER TABLE `indxalum`
  ADD PRIMARY KEY (`id_ixa`);

--
-- Indices de la tabla `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`id_log`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`id_materia`);

--
-- Indices de la tabla `matxalum`
--
ALTER TABLE `matxalum`
  ADD PRIMARY KEY (`id_mxa`);

--
-- Indices de la tabla `matxcur`
--
ALTER TABLE `matxcur`
  ADD PRIMARY KEY (`id_matxcur`);

--
-- Indices de la tabla `matxpro`
--
ALTER TABLE `matxpro`
  ADD PRIMARY KEY (`id_mxp`);

--
-- Indices de la tabla `planillas`
--
ALTER TABLE `planillas`
  ADD PRIMARY KEY (`id_planillas`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id_profesor`);

--
-- Indices de la tabla `tipo_user`
--
ALTER TABLE `tipo_user`
  ADD PRIMARY KEY (`tipo_u`);

--
-- Indices de la tabla `trabajos`
--
ALTER TABLE `trabajos`
  ADD PRIMARY KEY (`id_trabajo`);

--
-- Indices de la tabla `traxalum`
--
ALTER TABLE `traxalum`
  ADD PRIMARY KEY (`id_txa`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `id_alumno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT de la tabla `asistenciaalum`
--
ALTER TABLE `asistenciaalum`
  MODIFY `id_asisalum` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `asistenciaprof`
--
ALTER TABLE `asistenciaprof`
  MODIFY `id_asisprof` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT de la tabla `cuotas`
--
ALTER TABLE `cuotas`
  MODIFY `id_cuota` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `dias`
--
ALTER TABLE `dias`
  MODIFY `id_dia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `enfasis`
--
ALTER TABLE `enfasis`
  MODIFY `id_enfasis` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `horarios`
--
ALTER TABLE `horarios`
  MODIFY `id_horario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=235;

--
-- AUTO_INCREMENT de la tabla `indicadores`
--
ALTER TABLE `indicadores`
  MODIFY `id_indicador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=210;

--
-- AUTO_INCREMENT de la tabla `indxalum`
--
ALTER TABLE `indxalum`
  MODIFY `id_ixa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=315;

--
-- AUTO_INCREMENT de la tabla `log`
--
ALTER TABLE `log`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `id_materia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `matxalum`
--
ALTER TABLE `matxalum`
  MODIFY `id_mxa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=401;

--
-- AUTO_INCREMENT de la tabla `matxcur`
--
ALTER TABLE `matxcur`
  MODIFY `id_matxcur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=108;

--
-- AUTO_INCREMENT de la tabla `matxpro`
--
ALTER TABLE `matxpro`
  MODIFY `id_mxp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT de la tabla `planillas`
--
ALTER TABLE `planillas`
  MODIFY `id_planillas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `id_profesor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT de la tabla `tipo_user`
--
ALTER TABLE `tipo_user`
  MODIFY `tipo_u` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `trabajos`
--
ALTER TABLE `trabajos`
  MODIFY `id_trabajo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=114;

--
-- AUTO_INCREMENT de la tabla `traxalum`
--
ALTER TABLE `traxalum`
  MODIFY `id_txa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
