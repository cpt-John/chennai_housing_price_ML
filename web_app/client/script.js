/*fields template:{
'AREA': 'Karapakkam',
'INT_SQFT': 1004,
'DATE_SALE': '04-05-2011',
'N_BEDROOM': 1.0,
'N_BATHROOM': 1.0,
'N_ROOM': 3,
'SALE_COND': 'AbNormal',
'PARK_FACIL': 'Yes',
'DATE_BUILD': '15-05-1967',
'BUILDTYPE': 'Commercial',
'UTILITY_AVAIL': 'AllPub',
'STREET': 'Paved',
'MZZONE': 'A'
}*/
const field_data = {
  AREA: {
    f_name: "Area",
    type: "dropdown",
    values: [
      "Karapakkam",
      "Anna Nagar",
      "Adyar",
      "Velachery",
      "Chrompet",
      "KK Nagar",
      "T Nagar",
      "Velchery",
      "Ann Nagar",
    ],
  },
  INT_SQFT: { f_name: "Interior Sq.Ft", type: "input", range: [100, 4000] },
  DATE_SALE: { f_name: "Sale Date", type: "date" },
  N_BEDROOM: { f_name: "Bedrooms", type: "slider", range: [1, 10] },
  N_BATHROOM: { f_name: "Bathrooms", type: "slider", range: [1, 10] },
  N_ROOM: { f_name: "Total Rooms", type: "slider", range: [2, 25] },
  SALE_COND: {
    f_name: "Sale Condition",
    type: "dropdown",
    values: ["AbNormal", "Family", "Partial", "Normal Sale", "Adj Land"],
  },
  PARK_FACIL: {
    f_name: "Parking facility",
    type: "radio",
    values: ["yes", "no"],
    name_: "park",
  },
  DATE_BUILD: { f_name: "Built Date", type: "date" },
  BUILDTYPE: {
    f_name: "Build Type",
    type: "dropdown",
    values: ["Commercial", "Other", "House"],
  },
  UTILITY_AVAIL: {
    f_name: "Utility",
    type: "dropdown",
    values: ["AllPub", "ELO", "NoSewr"],
  },
  STREET: {
    f_name: "Road",
    type: "dropdown",
    values: ["Paved", "Gravel", "No Access"],
  },
  MZZONE: {
    f_name: "Zone",
    type: "radio",
    values: ["A", "RH", "RL", "I", "C", "RM"],
    name_: "zone",
  },
};

const components = {
  input: (object) => `<input
      class="input"
      type="number"
      min="${object.range[0]}"
      max="${object.range[1]}"
      class="floatLabel"
      name="Squareft"
      value="1000"
      id="${object.id}"
    />`,

  radio: (object) => `<div class="switch-field" id="${object.id}">
  ${object.values
    .map((element, i) => {
      return `<input
      type="radio"
      id="radio-${object.name_}-${i}"
      value="${element}"
      name="${object.name_}"
      ${!i ? " checked" : ""}/>
    <label for="radio-${object.name_}-${i}">${element}</label>`;
    })
    .join(" ")}
    </div>`,

  dropdown: (object) => `<select class="location" id="${object.id}">
      ${object.values
        .map((element, i) => {
          return `${!i ? "<option selected>" : "<option>"}${element}</option>`;
        })
        .join(" ")}
    </select>`,

  slider: (object) => `<input
      type="range"
      min="${object.range[0]}"
      max="${object.range[1]}"
      value="${object.range[0]}"
      class="slider"
      id="${object.id}"
    /><output>${object.range[0]}</output>`,

  date: (object) => `<input type="date"  value="2010-12-31"
  min="01-01-1949" max="31-12-2030" id="${object.id}"/>`,
};

function getValues() {
  const object = {};
  for (const field in field_data) {
    type = field_data[field]["type"];
    object[field] =
      type == "radio"
        ? $(`input[name="${field_data[field]["name_"]}"]:checked`).val()
        : $(`#${field}`).val();
  }
  const correct_dt_fmt = (dt_str) => {
    return dt_str.split("-").reverse().join("-");
  };
  ["DATE_SALE", "DATE_BUILD"].forEach((e) => {
    object[e] = correct_dt_fmt(object[e]);
  });
  return object;
}

function updateNRooms() {
  const n_room = Number($("#N_BEDROOM").val()) + Number($("#N_BATHROOM").val());
  const current = $(this);
  current.next().html(current.val());
  if (n_room > Number($("#N_ROOM").val())) {
    $("#N_ROOM").val(String(n_room));
    $("#N_ROOM").next().val(String(n_room));
  }
}

function setDate() {
  const b_date = new Date($("#DATE_BUILD").val()).getTime();
  const s_date = new Date($("#DATE_SALE").val()).getTime();
  if (b_date > s_date) {
    $("#DATE_BUILD").val($("#DATE_SALE").val());
  }
}

function setRange(range, element) {
  const value = Number($(element).val());
  if (!(value >= range[0] && value <= range[1])) {
    $(element).val(range[0]);
  }
}

function onClickedEstimatePrice() {
  estPriceRange = document.getElementById("uiEstimatedPriceRange");
  estPrice = document.getElementById("uiEstimatedPrice");
  const object = getValues();
  var url = "http://127.0.0.1:5000/predict_home_price";
  var formatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumSignificantDigits: 5,
  });

  formatter.format(2500);
  $.post(url, object, function (data) {
    // {'lower': 7219814,'mid': 767932,'upper': 803481}
    for (const [key, value] of Object.entries(data)) {
      data[key] = formatter.format(Number(value)).replace(/^(\D+)/, "$1 ");
    }
    estPriceRange.innerHTML = `<h1 class="result-text">${data.lower} - ${data.upper}</h1>`;
    estPrice.innerHTML = `<h1 class="result-text">Fair price: ${data.mid}</h1>`;
  });
}

function onPageLoad() {
  for (const field in field_data) {
    const object = { ...field_data[field], id: field };
    let html = components[object["type"]](object);
    const header = `<h2>${object["f_name"]}</h2>`;
    html = `<div class="component">${header}${html}</div>`;
    $("#form").append(html);
  }
  ["N_BEDROOM", "N_BATHROOM", "N_ROOM"].forEach(function (e) {
    $(`#${e}`).on("change", updateNRooms);
  });
  ["DATE_SALE", "DATE_BUILD"].forEach(function (e) {
    $(`#${e}`).on("change", setDate);
  });
  $("#INT_SQFT").on("change", function (event) {
    const range = field_data["INT_SQFT"].range;
    setRange(range, this);
  });
}

window.onload = onPageLoad;
