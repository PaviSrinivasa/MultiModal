var action, type;
var selected_dir_id, selected_file;
var zclip = false;

function size() {
    $('#main').height($(window).height() - 47);
    $('#left').height($(window).height() - 69);
    $('#right').height($(window).height() - 69);
    $('#content').height($(window).height() - 69);
}

function onload() {
    size();
    refresh_dirs();
    show_files();
    $('body').bind('click', function (e) {
        $('#dir-menu').hide();
        $('.unzip-menu').hide();
        $('#file-menu').hide();
    });
}

$('body').ready(onload);
$(window).resize(size);

function refresh_dirs() {
    $('#left').html(show_directories(dir_structure));
}

function get_dir(ds) {
    if (!ds) ds = dir_structure;
    dir = null;
    for (d in ds) {
        dir = ds[d];
    }
    return dir;
}

function get_files(ds){
    if (!ds) ds= dir_structure;
    for(f in ds){
        files_list = ds[d]['files'];
    }
    return files_list;
}

function change_sign() {
    d = get_dir();
    if (d['open'] == 'yes') d['open'] = 'no';
    else d['open'] = 'yes';
    refresh_dirs();
}

function get_name(ds) {
    for (d in ds) {
        name_dir = ds[d]['name'];
    }
    return name_dir;
}
function get_dirlist(ds) {
    for (d in ds) {
        dir_list = ds[d]['dirs'];
    }
    return dir_list;
}

function show_files(folderurl) {
    this.folder = folderurl;
    var dirs = [];
    var dir_list = get_dirlist(dir_structure)
    var name_folders = get_name(dir_structure)

    files = get_files().sort(
          function(a, b) {
            if (a.toLowerCase() < b.toLowerCase()) return -1;
            if (a.toLowerCase() > b.toLowerCase()) return 1;
            return 0;
          });

    $('#content').html('');

    var folderpath;

    for (i in dir_list){
        folderpath = dir_list[i]
        var filename = folderpath.toString().replace(/^.*[\\/]/, '');
        $('#content').append("<div class='file' title='" + filename + "'" +
            "ondblclick=\"show_files(" +  folderpath + ")\"><div class='thumbnail'>" +
            "<div style=\"background-image:url('" + static_url + "filemanager/images/folder_big.png');\" width='100%' height='100%' ></div></div>" +
            "<div class='filename'>" + filename + "</div></div>\n");
    }
    for(f in files) {
        var ext = files[f].split('.')[(files[f].split('.').length-1)];
        $('#content').append("<div class='file' title='"+escape(files[f])+"'"+
       "><div class='thumbnail'>"+
       "<div style=\"background-image:url('"+files[f]+"');\" width='100%' height='100%' ></div></div>"+
       "<div class='filename'>"+files[f]+"</div></div>\n");
    }
    $('.current_directory').removeClass('current_directory');
    $('#').addClass('current_directory');
}

function show_directories(ds) {
    var html = "";
    var d_list = false;
    for (d in ds) {
        var image = (ds[d]['open'] == 'yes' ? 'opened_folder.png' : 'folder.png');
        if (d == '') image = 'home_folder.png';
        var sign;
        sign = (ds[d]['open'] == 'yes' ? '[-]' : '[+]');
        var empty = true;
        for (i in ds[d]['dirs']) {
            empty = false;
            d_list = true;
            break;
        }
        if (empty) sign = '';
        var name_folder = ds[d]['name']

        html += "<div class='directory'> <div class='directory-sign' onclick='change_sign()'>" + sign + "</div>" +
            "<div class='directory-image-name' onmousedown='rightclick_handle(event,\"dir\");'>" +
            "<img class='directory-image' src='" + static_url + "filemanager/images/" + image + "'/>" +
            "<div class='directory-name' >" + (d == '' ? 'root' : d) + "</div></div></div>\n";
        if (ds[d]['open'] == 'yes' && d_list) {
            for(i in name_folder) {
                html += "<div style='padding-left:15px'>"+ "<div class='directory-sign' onclick='change_sign()'>" + sign + "</div>" +
                    "<div class='directory-image-name' onclick='show_files(" + name_folder[i] + ")' onmousedown='rightclick_handle(event,\"dir\");'>" +
                    "<img class='directory-image' src='" + static_url + "filemanager/images/" + image + "'/>" +
                    "<div class='directory-name' >" + name_folder[i] + "</div></div></div></div>\n";
            }
        }
    }
    return html;
}
