
const MY_COLOR = 'green';
const OTHER_COLOR = 'red';
let map;
function loadJson(selector) {
    return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

initMap = () => {
    map = new ymaps.Map("map", {
        center: [54.514403, 36.259522],
        zoom: 14
    });   
    let trackers = loadJson('#jsonData');
    trackers.forEach(function(tracker) {
        addMark(tracker["tracker_id"],tracker["lat"],tracker["lon"],tracker["tracker_name"]);
      });   
}

let marks = new Map();

addMark = (id, latitude, longitude, name = username, color = MY_COLOR) => {
    let mark = new ymaps.Placemark([latitude, longitude], {
        balloonContentHeader: name,
    }, {
        preset: `islands#${color}CircleDotIcon`,
    });
    map.geoObjects.add(mark);
    marks.set(id, mark);
}

removeMark = (id) => {
    let mark = marks.get(id);
    map.geoObjects.remove(mark);
    marks.delete(id);
}