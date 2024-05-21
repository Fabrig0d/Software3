CALL insertar_tipoProd('Algas Marinas y Fitohormonas');
CALL insertar_tipoProd('Fungicidas Biológicos');
CALL insertar_tipoProd('Aminoácidos');
CALL insertar_tipoProd('Ácidos Húmicos');
CALL insertar_tipoProd('Nutrientes Específicos');	

-- FITO ALGAS: Algas Marinas + Fitohormonas
CALL insertar_prod('FITO ALGAS', 'Algas Marinas + Fitohormonas', '12 litros', 30.00, 50.00, 100, 1);
CALL insertar_prod('FITO ALGAS', 'Algas Marinas + Fitohormonas', '20 litros', 25.00, 40.00, 150, 1);
CALL insertar_prod('FITO ALGAS', 'Algas Marinas + Fitohormonas', '200 litros', 20.00, 35.00, 200, 1);

-- ALGAS SHEER: Algas marinas
CALL insertar_prod('ALGAS SHEER', 'Algas marinas', '12 litros', 20.00, 35.00, 80, 1);
CALL insertar_prod('ALGAS SHEER', 'Algas marinas', '20 litros', 15.00, 30.00, 120, 1);
CALL insertar_prod('ALGAS SHEER', 'Algas marinas', '200 litros', 10.00, 20.00, 50, 1);

-- HONGO STOP: Fungicida Biológico
CALL insertar_prod('HONGO STOP', 'Fungicida Biológico', '12 litros', 55.00, 65.00, 90, 2);
CALL insertar_prod('HONGO STOP', 'Fungicida Biológico', '20 litros', 45.00, 60.00, 110, 2);
CALL insertar_prod('HONGO STOP', 'Fungicida Biológico', '200 litros', 40.00, 55.00, 150, 2);

-- FITO AMINO: Aminoácidos
CALL insertar_prod('FITO AMINO', 'Aminoácidos', '12 litros', 35.00, 60.00, 70, 3);
CALL insertar_prod('FITO AMINO', 'Aminoácidos', '20 litros', 30.00, 50.00, 100, 3);
CALL insertar_prod('FITO AMINO', 'Aminoácidos', '200 litros', 25.00, 50.00, 130, 3);

-- FITO HUMIC 20: Ácidos Húmicos (Leonardita)
CALL insertar_prod('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '12 litros', 15.00, 20.00, 60, 4);
CALL insertar_prod('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '20 litros', 11.00, 15.00, 80, 4);
CALL insertar_prod('FITO HUMIC 20', 'Ácidos Húmicos (Leonardita)', '200 litros', 8.00, 15.00, 100, 4);

-- Nutrientes Específicos (Potasio, Fósforo, Boro, Calcio, Magnesio)
CALL insertar_prod('FITO K – 50', 'Potasio', '12 litros', 18.00, 28.00, 50, 5);
CALL insertar_prod('FITO K – 50', 'Potasio', '20 litros', 16.00, 25.00, 70, 5);
CALL insertar_prod('FITO K – 50', 'Potasio', '200 litros', 13.00, 20.00, 90, 5);

CALL insertar_prod('FITO POWER', 'Fósforo', '12 litros', 18.00, 28.00, 40, 5);
CALL insertar_prod('FITO POWER', 'Fósforo', '20 litros', 16.00, 25.00, 60, 5);
CALL insertar_prod('FITO POWER', 'Fósforo', '200 litros', 13.00, 20.00, 80, 5);

CALL insertar_prod('FITO BORO', 'Boro', '12 litros', 18.00, 28.00, 30, 5);
CALL insertar_prod('FITO BORO', 'Boro', '20 litros', 16.00, 25.00, 50, 5);
CALL insertar_prod('FITO BORO', 'Boro', '200 litros', 13.00, 20.00, 70, 5);

CALL insertar_prod('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '12 litros', 18.00, 28.00, 80, 5);
CALL insertar_prod('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '20 litros', 16.00, 25.00, 100, 5);
CALL insertar_prod('FITO Ca/B/Zn', 'Calcio, Boro, Zinc', '200 litros', 13.00, 20.00, 120, 5);

CALL insertar_prod('FITO MAGNESIO', 'Magnesio', '12 litros', 18.00, 28.00, 60, 5);


CALL listar_tipoProd();
DESC productos;
CALL listar_prod();

-- Insertar 10 registros adicionales de clientes utilizando el procedimiento almacenado
CALL insertar_cli('11111111', 'Ana', 'López', 'ana@example.com', 'Calle Ancha 111');
CALL insertar_cli('22222222', 'Pedro', 'Sánchez', 'pedro@example.com', 'Avenida del Sol 222');
CALL insertar_cli('33333333', 'Laura', 'García', 'laura@example.com', 'Plaza Central 333');
CALL insertar_cli('44444444', 'Miguel', 'Rodríguez', 'miguel@example.com', 'Calle Estrecha 444');
CALL insertar_cli('55555555', 'Sofía', 'Fernández', 'sofia@example.com', 'Avenida del Río 555');
CALL insertar_cli('66666666', 'Manuel', 'González', 'manuel@example.com', 'Calle Larga 666');
CALL insertar_cli('77777777', 'Elena', 'Díaz', 'elena@example.com', 'Avenida de la Luna 777');
CALL insertar_cli('88888888', 'David', 'Pérez', 'david@example.com', 'Plaza del Pueblo 888');
CALL insertar_cli('99999999', 'Carmen', 'Muñoz', 'carmen@example.com', 'Calle Nueva 999');
CALL insertar_cli('10101010', 'Antonio', 'Ruiz', 'antonio@example.com', 'Avenida de la Playa 1010');
