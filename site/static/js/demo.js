var events = [
    {'Date': new Date(2021, 5, 7), 'Title': 'サンプル1'},
    {'Date': new Date(2021, 5, 18), 'Title': 'サンプル2'},
    {'Date': new Date(2021, 5, 27), 'Title': 'サンプル3'},
  ];
  
  var settings = {};
  var element = document.getElementById('caleandar');
  caleandar(element, events, settings);