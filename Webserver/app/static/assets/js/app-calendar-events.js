"use strict"; 
let date = new Date,
nextDay = new Date((new Date).getTime() + 864e5),
nextMonth = 11 === date.getMonth() ? new Date(date.getFullYear() + 1, 0, 1) : new Date(date.getFullYear(),
date.getMonth() + 1, 1), prevMonth = 11 === date.getMonth() ? new Date(date.getFullYear() - 1, 0, 1) : new Date(date.getFullYear(), date.getMonth() - 1, 1);

var events = [];

xhr = new XMLHttpRequest();
xhr.open("GET", '/event/json/get', true);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.onload = function () {
    let data = JSON.parse(this.responseText);

    for (let key in data){
        let e = data[key];
        let NewEvent = {
            id: e.id,
            url: e.url,
            title: e.title,
            start:  new Date(e.start),
            end: new Date(e.end ),
            allDay: e.allDay,
            extendedProps: e.extendedProps
        };
        
        events.push(NewEvent);
    };

    let buttonselectAll = document.getElementById('selectAll');
    buttonselectAll.click();buttonselectAll.click();
}

xhr.send();
console.log(events)