$(document).ready(function(){
        var departamentos = {
            "Amazonas": {
                "Chachapoyas": ["Chachapoyas", "Bagua", "Bongará"],
                "Bagua": ["Bagua Grande", "El Parco", "Imaza"]
            },
            "Áncash": {
                "Huaraz": ["Huaraz", "Carhuaz", "Yungay"],
                "Aija": ["Aija", "Coris", "Huacllán"]
            },
            "Apurímac": {
                "Abancay": ["Abancay", "Circa", "Tamburco"],
                "Andahuaylas": ["Andahuaylas", "Andarapa", "Chiara"]
            },
            "Arequipa": {
                "Arequipa": ["Arequipa", "Camaná", "Islay"],
                "Islay": ["Mollendo", "Cocachacra"]
            },
            "Ayacucho": {
                "Huamanga": ["Huamanga", "Acocro", "Acos Vinchos"],
                "Huanta": ["Huanta", "Ayahuanco", "Huancaray"]
            },
            "Cajamarca": {
                "Cajamarca": ["Cajamarca", "Asunción", "Chetilla"],
                "Cajabamba": ["Cajabamba", "Cachachi", "Condebamba"]
            },
            "Callao": {
                "Callao": ["Callao"]
            },
            "Cusco": {
                "Cusco": ["Cusco", "Ccorca", "Poroy"],
                "Anta": ["Anta", "Ancahuasi", "Huarocondo"]
            },
            "Huancavelica": {
                "Huancavelica": ["Huancavelica", "Acobambilla", "Acoria"],
                "Tayacaja": ["Pampas", "Acostambo", "Anchonga"]
            },
            "Huánuco": {
                "Huánuco": ["Huánuco", "Amarilis", "Chinchao"],
                "Leoncio Prado": ["Tingo María", "Chaglla", "Molino"]
            },
            "Ica": {
                "Ica": ["Ica", "La Tinguiña", "Los Aquijes"],
                "Chincha": ["Chincha Alta", "Alto Laran", "Chavin"]
            },
            "Junín": {
                "Huancayo": ["Huancayo", "Carhuacallanga", "Chacapampa"],
                "Jauja": ["Jauja", "Acolla", "Apata"]
            },
            "La Libertad": {
                "Trujillo": ["Trujillo", "El Porvenir", "Florentino Ameghino"],
                "Ascope": ["Ascope", "Chicama", "Paiján"]
            },
            "Lambayeque": {
                "Chiclayo": ["Chiclayo", "Chongoyape", "Eten"],
                "Ferreñafe": ["Ferreñafe", "Cañaris", "Incahuasi"]
            },
            "Lima": {
                "Lima": ["Lima", "Cajatambo", "Canta"],
                "Cañete": ["San Vicente", "Asia", "Mala"]
            },
            "Loreto": {
                "Iquitos": ["Iquitos", "Alto Nanay", "Fernando Lores"],
                "Maynas": ["Nauta", "Indiana", "Pebas"]
            },
            "Madre de Dios": {
                "Tambopata": ["Tambopata", "Inambari", "Las Piedras"]
            },
            "Moquegua": {
                "Mariscal Nieto": ["Moquegua", "Carumas", "Cuchumbaya"]
            },
            "Pasco": {
                "Pasco": ["Pasco", "Chaupimarca", "Huachón"],
                "Oxapampa": ["Oxapampa", "Chontabamba", "Huancabamba"]
            },
            "Piura": {
                "Piura": ["Piura", "Cura Mori", "La Arena"],
                "Sullana": ["Sullana", "Bellavista", "Ignacio Escudero"]
            },
            "Puno": {
                "Puno": ["Puno", "Acora", "Amantani"],
                "San Román": ["Juliaca", "Acora", "Ácora"]
            },
            "San Martín": {
                "Moyobamba": ["Moyobamba", "Calzada", "Habana"],
                "Bellavista": ["Bellavista", "Alto Biavo", "Bajo Biavo"]
            },
            "Tacna": {
                "Tacna": ["Tacna", "Alto de la Alianza", "Calana"]
            },
            "Tumbes": {
                "Tumbes": ["Tumbes", "Corrales", "La Cruz"],
                "Zarumilla": ["Zarumilla", "Aguas Verdes", "Matapalo"]
            },
            "Ucayali": {
                "Coronel Portillo": ["Pucallpa", "Calleria", "Campo Verde"]
            }
        };
    
        // Función para cargar las provincias de un departamento
        function cargarProvincias(departamento){
            var provincias = departamentos[departamento];
            var provinciaOptions = '';
            for(var provincia in provincias){
                provinciaOptions += '<option value="' + provincia + '">' + provincia + '</option>';
            }
            $("#c_provincia").html(provinciaOptions);
        }
        // Función para cargar los distritos de una provincia
        function cargarDistritos(departamento, provincia){
            var distritos = departamentos[departamento][provincia];
            var distritoOptions = '';
            for(var i = 0; i < distritos.length; i++){
                distritoOptions += '<option value="' + distritos[i] + '">' + distritos[i] + '</option>';
            }
            $("#c_distrito").html(distritoOptions);
        }
    
        // Maneja el cambio en el campo de selección de departamento
        $("#c_departamento").change(function(){
            var departamento = $(this).val();
            cargarProvincias(departamento); // Solo pasar el departamento
        });
    });