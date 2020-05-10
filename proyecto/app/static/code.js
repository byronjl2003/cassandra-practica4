$("#idFormPais").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormPais");
    var y = document.getElementById("infopais");
    y.innerHTML = '<p class="loading">Creando pais</p>'
    var data = new FormData(form);

    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/postpais',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});

$('#selfronteras').change(function(){
    xx = ""+$(this).val();
    //console.log(xx);
    var y = document.getElementById("dinamicopais");
    //e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormPais");
    //var y = document.getElementById("reporte1");
    //y.innerHTML = '<p>...Ejecutando...';
    var data = new FormData(form);
    /*
    var x = document.getElementById("divspinner");
   
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    */
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/setfrontera',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


    

});




//-----------------TERMINAN COSAS DEL INGRESO DE PAIS--------------------
//-----------------EMPIESAN COSAS PARA EL INGRESO DE LOS COLABORADORES----------
$("#idFormcolaboradores").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormcolaboradores");
    var y = document.getElementById("infocolaborador");
    y.innerHTML = '<p class="loading">Creando colaborador</p>'
    var data = new FormData(form);

    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/postcolaborador',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});

$('#selareas').change(function(){
    xx = ""+$(this).val();
    //console.log(xx);
    var y = document.getElementById("dinamicocolaboradores");
    //e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormcolaboradores");
    //var y = document.getElementById("reporte1");
    //y.innerHTML = '<p>...Ejecutando...';
    var data = new FormData(form);
    /*
    var x = document.getElementById("divspinner");
   
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    */
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/setareacolaborador',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


    

});






//----------------- TERMINAN COSAS PARA EL INGRESO DE COLABORADORES
//##################EMPIEZAN LAS COSAS PARA EL INGRESO DE LAS PATENTES
//dinamico de pais no.. por que solo se escoje uno..
$('#selinventores1').change(function(){
    xx = ""+$(this).val();
    //console.log(xx);
    var y = document.getElementById("dinamico");
    //e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormpatentes");
    //var y = document.getElementById("reporte1");
    //y.innerHTML = '<p>...Ejecutando...';
    var data = new FormData(form);
    /*
    var x = document.getElementById("divspinner");
   
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    */
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/set_inventorespatente',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });

});

$('#selareas1').change(function(){
    xx = ""+$(this).val();
    //console.log(xx);
    var y = document.getElementById("selcolaboradores1");
    //e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormpatentes");
    //var y = document.getElementById("reporte1");
    //y.innerHTML = '<p>...Ejecutando...';
    var data = new FormData(form);
    /*
    var x = document.getElementById("divspinner");
   
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    */
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/get_colaboradores',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


    

});
$('#selcolaboradores1').change(function(){
    xx = ""+$(this).val();
    //console.log(xx);
    var y = document.getElementById("dinamico");
    //e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormpatentes");
    //var y = document.getElementById("reporte1");
    //y.innerHTML = '<p>...Ejecutando...';
    var data = new FormData(form);
    /*
    var x = document.getElementById("divspinner");
   
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    */
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/set_colaboradorespatente',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


    

});

$("#idFormpatentes").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormpatentes");
    //var y = document.getElementById("divcards");
    var y = document.getElementById("infopatentes");
    var data = new FormData(form);
    y.innerHTML = '<p class="loading">Cargando paises</p>'
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/setpatente',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});


//###############################################TERMINA LAS ONDAS PARA EL INGRESO DE PATENTES


//#############################REPORTEE
$("#idFormreporte1").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormreporte1");
    var y = document.getElementById("inforeporte1");
    y.innerHTML = '<p class="loading">Calculando reporte</p>'
    var data = new FormData(form);

    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/getreporte1',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});
$("#idFormreporte2").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormreporte2");
    var y = document.getElementById("inforeporte2");
    y.innerHTML = '<p class="loading">Calculando reporte</p>'
    var data = new FormData(form);

    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/getreporte2',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});
$("#idFormreporte3").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormreporte3");
    var y = document.getElementById("inforeporte3");
    y.innerHTML = '<p class="loading">Calculando reporte</p>'
    var data = new FormData(form);

    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/getreporte3',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});

///////////////////////////////////////////////////
function myFunction() {
    var x = document.getElementById("divspinner");
    var y = document.getElementById("divtable");
    var frec = document.getElementById("inputLarge");

    var dataa = 0;

    if (document.getElementById("customRadio1").checked) {
        dataa = { frecuencia: frec.value, tipo: 1 };
    } else {

        dataa = { frecuencia: frec.value, tipo: 0 };
    }
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {

    }
    $.ajax({
            method: "POST",
            url: "http://localhost:8080/generar",
            data: dataa
        })
        .done(function(msg) {
            x.style.display = "none";
            y.innerHTML += msg;
            console.log(msg);
            y.style.display = "block";

        });
}

function uploadd() {
    var x = document.getElementById("inputGroupFile02");
    var formdata = new FormData();
    var file = x.files[0];
    formdata.append("file", file);
    $.ajax({
            method: "POST",
            url: "http://localhost:8080/filtrar",
            data: file,
            processData: false,
            contentType: false
        })
        .done(function(msg) {
            console.log(msg);
        });

}

$( function() {
    $( "#datepickercolaboradores" ).datepicker({
        dateFormat: "yy-mm-dd"
      });
    $( "#datepicker1" ).datepicker({
        dateFormat: "yy-mm-dd"
      });
    $( "#datepicker2" ).datepicker({
        dateFormat: "yy-mm-dd"
      });
    $( "#datepicker3" ).datepicker({
        dateFormat: "yy-mm-dd"
      });
    $( "#datepicker4" ).datepicker({
        dateFormat: "yy-mm-dd"
      });
    $( "#datepicker5" ).datepicker({
        dateFormat: "yy-mm-dd"
      });

      
  } );


