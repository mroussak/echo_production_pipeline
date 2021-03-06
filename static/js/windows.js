// Load the left window gif views

$(function() {
    var i = 0;
    $.each(jsonObject, function(key, value) {
        // var currObj = value;
        
        $.each(currObj['dicoms'], function(key, value) {
            var dicomObj = value;
            i++;
            document.getElementById('thumbnails').innerHTML += '<section><div title="Drag and drop me in one of the panes to the right" class="gif-div draggable"><img class="gif-img draggable" id="' + dicomObj['dicom_id'] + '" src="https://app.icardio.ai' + dicomObj['paths']['path_to_dicom_gif'] + '"></div><div class="controls"></div><h3 class="view">' + currObj['view'] + '</h3></section>';
            var image = '<img class="analysis-img" src="https://app.icardio.ai/' +dicomObj['paths']['path_to_dicom_gif'] + '">"';
//           old button  <a class="waves-effect waves-light btn analysis-button modal-trigger" href="#modal1">Analyze</a>
            return dicomObj;
        });
    });
});

//if no views detected
document.getElementById('thumbnails').innerHTML += "No views detected.";


//drag and drop controllers 
var playing_clip;
var playing_clip_top;
var playing_clip_bottom;

$(function() {
    var draggedDicomId;
    $(".draggable").draggable({
        cursor: "pointer"
    }, {
        revert: true
    }, {
        revertDuration: 100
    }, {
        drag: function(event, ui) {
            draggedDicomId = $(this).attr("id");
        }
    });
    $(".top").droppable({
        drop: function(event, ui) {
            $(".top").html(displayConsole(draggedDicomId));
            if (playing_clip_top != undefined){
                clearInterval(playing_clip_top);
            }
            defineImgIndex(draggedDicomId);
            playing_clip_top = play_clip();
        }
    });
    $(".bottom").droppable({
        drop: function(event, ui) {
            $(".bottom").html(displayConsole(draggedDicomId));
            if (playing_clip_bottom != undefined){
                clearInterval(playing_clip_bottom);
            }
            defineImgIndex(draggedDicomId);
            playing_clip_bottom = play_clip();
        }
    });
});


//display the html in each view panel
function displayConsole(draggedDicomId){
    var reportControls = setViewControls(draggedDicomId, getJsonDetail(draggedDicomId, 'predicted_view'));
    var html = `
<div class="split-display left">
    <p class="meta-text-left">Frame <span class="${draggedDicomId}">1</span>/${ getJsonDetail(draggedDicomId, 'config', 'number_of_frames') }</p>
    <p class="meta-text-center">${draggedDicomId}</p>
    <p class="meta-text-right">${ getJsonDetail(draggedDicomId, 'predicted_view') }</p>
    <div class="analysis-div">
    <img class="analysis-img ${draggedDicomId}" src="${ getJsonDetail(draggedDicomId, 'paths', 'path_to_dicom_jpeg', 0) }" data-id="${draggedDicomId}" img-analysis1">
    </div>
</div>
<div class="split-display right">
    <p class="meta-text-left">Frame <span class="${draggedDicomId}">1</span>/${ getJsonDetail(draggedDicomId, 'config', 'number_of_frames') }</p>
    <p class="meta-text-center">${draggedDicomId}</p>
    <p class="meta-text-right">${ getJsonDetail(draggedDicomId, 'predicted_view') }</p>
    <div class="analysis-div">
        <img class="analysis-img ${draggedDicomId}" data-directory="${ getDefaultDataDirectory(getJsonDetail(draggedDicomId, 'predicted_view'))}" src="https://app.icardio.ai${ getJsonDetail(draggedDicomId, 'paths', getDefaultDataDirectory(getJsonDetail(draggedDicomId, 'predicted_view')), 0) }" data-id="${draggedDicomId}" img-analysis1">
    </div>
</div>
<div class="report controls">
    ${reportControls}
</div>
    `;
    return html;
}

//change the image of each panel and update the directory
function changeImage(dir, dicomID, panel_direction) {
    var img = $(`.split-display.${panel_direction} .analysis-img[data-id="${dicomID}"]`).first();
    var img_source = img.attr("src");
    var second_directory = img.attr("data-directory");

    //assign primary directory
    image_directory = panel_direction == 'left' ? getJsonDetail(dicomID, 'paths', 'path_to_dicom_jpeg') : getJsonDetail(dicomID, 'paths', second_directory);
    
//     getJsonDetail(dicomID, 'path_to_simpsons_jpeg');
    
    const imgIndex = image_directory.indexOf(img_source)
    
    var newIndex;
    
    //controlling the left panel
    if ((imgIndex == 0) && dir == -1){
        newIndex = image_directory.length - 1;
    } else if ((imgIndex == image_directory.length - 1) && dir == 1) {
        newIndex = 0;
    } else {
        newIndex = imgIndex + dir;
    }
    
    img_source = image_directory[newIndex];
    
    
    img.attr("src", img_source);
    
    $(`.split-display.${panel_direction} .${dicomID}`).html(newIndex + 1);

}

function play_clip() {
    const play = setInterval(function(){
        $(".split-display.left .analysis-img").each(function(){
            var dicomID = $(this).attr('data-id');
            changeImage(1, dicomID, 'left') //left <- show Prev image
        });
        $(".split-display.right .analysis-img").each(function(){
            var dicomID = $(this).attr('data-id');
            changeImage(1, dicomID, 'right') //left <- show Prev image
        });
    }, 40); // sets the play clip interval in miliseconds
    return play;
}

//capture the arrow key navigations and 
document.onkeydown = (e) => {
    e = e || window.event;
    const isLeft = e.keyCode == '37';
    const isRight = e.keyCode == '39';
    if (isLeft || isRight) {
        clearInterval(playing_clip_top);
        clearInterval(playing_clip_bottom);
        var direction = isLeft ? -1 : 1;
        $(".split-display.left .analysis-img").each(function(){
            var dicomID = $(this).attr('data-id');
            changeImage(direction, dicomID, 'left') //left <- show Prev image
        });
        $(".split-display.right .analysis-img").each(function(){
            var dicomID = $(this).attr('data-id');
            changeImage(direction, dicomID, 'right') //left <- show Prev image
        });
    }
}

/*setInterval(function() {
    new Tippy('.report-button',{
        position:'top',
        animation:'perspective',
        interactive:'true'
    });
    console.log('1');
}, 1000);*/