

initMap = () => {
    map = new ymaps.Map("map", {
        center: [54.514403, 36.259522],
        zoom: 14
    });   
}

let marks = new Map();

addMark = (id, latitude, longitude, name, color = MY_COLOR) => {
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

showTrack = (jsontrack) => {
    map.geoObjects.remove(trackObMan);
    trackObMan = new ymaps.ObjectManager();
    trackObMan.add(jsontrack);
    map.geoObjects.add(trackObMan);
}
delTrack = () => {
    map.geoObjects.remove(trackObMan);
}