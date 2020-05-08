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

  $("#idForm").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idForm");
    //var y = document.getElementById("divcards");
    var x = document.getElementById("div-carga-paises");
    var data = new FormData(form);
    x.innerHTML = '<p class="loading">Cargando paises</p>'
    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: '/paises',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            x.innerHTML = '<p>Terminado</p>';
        }
    });


});
$("#FormCargaPatentes").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jujujuju');
    var form = document.getElementById("FormCargaPatentes");
    //var y = document.getElementById("divcards");
    var x = document.getElementById("div-carga-patentes");
    var data = new FormData(form);
    x.innerHTML = '<p class="loading">Cargando patentes</p>'
    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: '/carga_patentes',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            x.innerHTML = '<p>Terminado</p>';
        }
    });


});
$("#idForm2").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idForm2");
    var y = document.getElementById("reporte1");
    y.innerHTML = '<p>...Ejecutando...';
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
        url: '/reporte1',
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


$("#idForm3").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idForm3");
    var y = document.getElementById("reporte2");
    y.innerHTML = '<p>...Ejecutando...';
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
        url: '/reporte2',
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

