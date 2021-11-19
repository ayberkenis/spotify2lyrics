function get_datas() {
    $("#body").load( "api/v1/serve-live-data/ #body > *");

}
$(document).ready(function(){
    setInterval(get_datas, 5000)
});
