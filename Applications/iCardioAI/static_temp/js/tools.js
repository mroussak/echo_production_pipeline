// var jsonObject;
var file;
var images = [];


// if (window.location.href.indexOf("demo") > -1) {
//       file = 'demo';
//     } else {
//       file = 'reports';
//     }


// $(function(){
//   $.ajax({
//   url: '{% static "../static/Users/"%}{{user.username}}/Sessions/1/Reports/' + file + '.json?=_' + new Date().getTime(),
//   dataType: 'json',
//   async: false,
//   global: false,
//   success: function(data) {
//       jsonObject = data;
//   },
//       statusCode: {
//          404: function() {
//           console.log('There was a problem retrieving the JSON from the server.');
//          }
//       }
//     });

//     return {getDataObject : function()
//     {
//         if (jsonObject) return jsonObject;
//         // else show some error that it isn't loaded yet;
//     }};
// });
    
// jsonObject = jsonObject.getDataObject();

//unpack the JSON as needed
function getJsonDetail(selectedDicomID, detail, type, i){
    var int = 0;
    var detailToReturn;
    $.each(jsonObject, function(key, value) {
        var currObj = value;
        var index = 0;
        int++;
            $.each(currObj['dicoms'], function(key, value) {
            var dicomObj = value;
            index++;
            
            if ((dicomObj['dicom_id'] == selectedDicomID) && detail in dicomObj) {
                try {
                detailToReturn = type === undefined ? dicomObj[detail] : (i === undefined ? dicomObj[detail][type] : dicomObj[detail][type][i]);              
            } catch {
            console.log('Could not find: ' + selectedDicomID + detail + type + i);
            }
            }
        });
    });
return detailToReturn;
}

//preload images function

function preload() {
    for (var i = 0; i < arguments.length; i++) {
        images[i] = new Image();
        images[i].src = preload.arguments[i];
    }
}

function defineImgIndex(DicomId){
    var masterArray = [];
    var a = getJsonDetail(DicomId, 'paths');
    var index;
    for (var obj in a){
    	if(Array.isArray(a[obj])){
    // 		for (index = 0; index < a[obj].length; ++index){
    			masterArray = masterArray.concat(a[obj]);
            // }
		}
    }
    preload(masterArray)
}
    
//preload image usage: 


//update Json if needed
function updateJsonDetail(selectedDicomID, newParameter, value){
    var detailToUpdate;
    $.each(jsonObject, function(key, value) {
        var currObj = value;
        var index = 0;
            $.each(currObj['dicoms'], function(key, value) {
            var dicomObj = value;
            index++;
            if (dicomObj['dicom_id'] == selectedDicomID) {
                dicomObj[newParameter] = value;
            }
        });
    });
}

function getDefaultDataDirectory(view){
    if (view == 'A4C' || view == 'A2C') {return 'path_to_simpsons_jpeg';}
    else if (view == 'PSAX') { return 'path_to_cylinder_jpeg';} 
    else if (view == 'SUBA') { }
}



//set view controls
function setViewControls(dicomID, view) {
    if (view == undefined){
        var reportControls = '<a title="Drag a view into the pane to begin analysis" class="btn report-button" style="margin:0px -4px 0px 0px">No views selected.</a>'
        return reportControls;
    }
    if (view == 'A4C') {
        var reportControls =
        `<span class="tools-left">
            <a title="Ejection fraction (EF) is a measure of blood flow through the cardiac cycle. Ejection fraction is reported as a percentage of blood that leaves the left ventricle during each cycle. Low ejection fraction may be indicative of an unhealthy heart." class="btn report-button" style="margin:0px -4px 0px 0px">EF: ${Math.round(getJsonDetail(dicomID, 'metrics', 'ef'))}%</a>
            <a class="btn report-button" title="Left ventricle systolic volume (LVSV) is the volume of blood at systole measured in milliliters. It is calculated using the Simpson's method and is used to determine the ejection fraction.">LVSV: ${Math.round(getJsonDetail(dicomID, 'metrics', 'lvsv'))}ml </a>
            <a class="btn report-button" title="Left ventricle diastolc volume (LVDV) is the volume of blood at diastole measured in milliliters. It is calculated using the Simpson's method and is used to determine the ejection fraction.">LVDV: ${Math.round(getJsonDetail(dicomID, 'metrics','lvdv'))}ml </a>
            <a class="btn report-button" title="Left ventricle systolic diameter (LVSD) is the diameter of the left ventricle at systole measured in centimeters. It is calculated by drawing a line at the widest horizontal.">LVSD: ${(Math.round(getJsonDetail(dicomID, 'metrics','lvsd')*100)/100).toFixed(2)}cm </a>
            <a class="btn report-button" title="Left ventricle diastolic diameter (LVDD) is the diameter of the left ventricle at diastole measured in centimeters. It is calculated by drawing a line at the widest horizontal.">LVDD: ${(Math.round(getJsonDetail(dicomID, 'metrics','lvdd')*100)/100).toFixed(2)}cm </a>

        </span>
        <span class="tools-right">
            <a class="waves-effect waves-light btn analysis-button report-button" onclick="changeImageDirectory('${dicomID}','path_to_simpsons_jpeg');">Simpsons Calculation</a>
            <a class="waves-effect waves-light btn analysis-button report-button" onclick="changeImageDirectory('${dicomID}','path_to_mask_jpeg');">Original Segmentation</a>
        </span>`
        return reportControls;
    }
    if (view == 'A2C') {
        var reportControls =
        `<span class="tools-left">
            <a title="Ejection fraction (EF) is a measure of blood flow through the cardiac cycle. Ejection fraction is reported as a percentage of blood that leaves the left ventricle during each cycle. Low ejection fraction may be indicative of an unhealthy heart." class="btn report-button" style="margin:0px -4px 0px 0px" >EF: ${Math.round(getJsonDetail(dicomID, 'metrics', 'ef'))}%</a>
            <a class="btn report-button" title="Left ventricle systolic volume (LVSV) is the volume of blood at systole measured in milliliters. It is calculated using the Simpson's method and is used to determine the ejection fraction.">LVSV: ${Math.round(getJsonDetail(dicomID, 'metrics', 'lvsv'))}ml </a>
            <a class="btn report-button" title="Left ventricle diastolc volume (LVDV) is the volume of blood at diastole measured in milliliters. It is calculated using the Simpson's method and is used to determine the ejection fraction.">LVDV: ${Math.round(getJsonDetail(dicomID, 'metrics','lvdv'))}ml </a>
            <a class="btn report-button" title="Left ventricle systolic diameter (LVSD) is the diameter of the left ventricle at systole measured in centimeters. It is calculated by drawing a line at the widest horizontal.">LVSD: ${(Math.round(getJsonDetail(dicomID, 'metrics','lvsd')*100)/100).toFixed(2)}cm </a>
            <a class="btn report-button" title="Left ventricle diastolic diameter (LVDD) is the diameter of the left ventricle at diastole measured in centimeters. It is calculated by drawing a line at the widest horizontal.">LVDD: ${(Math.round(getJsonDetail(dicomID, 'metrics','lvdd')*100)/100).toFixed(2)}cm </a>

        </span>
        <span class="tools-right">
            <a class="waves-effect waves-light btn analysis-button report-button" onclick="changeImageDirectory('${dicomID}','path_to_simpsons_jpeg');">Simpsons Calculation</a>
            <a class="waves-effect waves-light btn analysis-button report-button" onclick="changeImageDirectory('${dicomID}','path_to_mask_jpeg');">Original Segmentation</a>
        </span>`
        return reportControls;
    }
    if (view == 'PSAX') {
        var reportControls =
        `<span class="tools-left">
            <a title="Ejection fraction in the Parasternal Short Axis View is ascertained using the Teichholz method. In this view, ejection fraction is measured by calculating the change in area of the left ventricle." class="btn report-button" style="margin:0px -4px 0px 0px" >EF: ${Math.round(getJsonDetail(dicomID, 'metrics', 'ef_teichholz'))}%</a>
            <a class="btn report-button" title="Left ventricle systolic volume (LVSV) is the volume of blood at systole. It is calculated using the Teichholz formula and is measured in milliliters.">LVSV: ${Math.round(getJsonDetail(dicomID, 'metrics', 'lvsv_teichholz'))}ml </a>
            <a class="btn report-button" title="Left ventricle diastolic volume (LVDV) is the volume of blood at diastole. It is calculated using the Teichholz formula and is measured in milliliters.">LVDV: ${Math.round(getJsonDetail(dicomID, 'metrics', 'lvdv_teichholz'))}ml </a>
         </span>
        <span class="tools-right">
            <a class="waves-effect waves-light btn analysis-button report-button" onclick="changeImageDirectory('${dicomID}','path_to_cylinder_jpeg');">Overlay Ellipse</a>
            <a class="waves-effect waves-light btn analysis-button report-button" onclick="changeImageDirectory('${dicomID}','path_to_mask_jpeg');">Original Segmentation</a>
        </span>`
        var img = $(`.split-display.right .analysis-img[data-id="${dicomID}"]`).first();
        img.attr("src", getJsonDetail(dicomID, 'paths', 'path_to_cylinder_jpeg', 0));
        return reportControls;
    }
}

function changeImageDirectory(DicomID,desiredDirectory) {
    var img = $(`.split-display.right .analysis-img[data-id="${DicomID}"]`).first();
    console.log(img);
    var img_source = img.attr("src");
    const imgIndex = image_directory.indexOf(img_source);
    var newDirec = getJsonDetail(DicomID, 'paths', desiredDirectory, imgIndex);
    console.log(img_source,newDirec)
    img.attr("src", newDirec);
    img.attr("data-directory", desiredDirectory);
}

// new Tippy('.gif-div',{
//     position:'top',
//     animation:'perspective',
//     interactive:'true'
//     });

//initialize modals
// $(document).ready(function(){
//     $('.modal').modal();
// });