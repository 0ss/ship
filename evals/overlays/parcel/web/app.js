const parcels = {
  "P-101": { address: "12 River Lane", area: "680 m²" },
  "P-102": { address: "4 Oak Street", area: "420 m²" },
};

function showParcel(id) {
  const parcel = parcels[id];
  if (!parcel) return;
  const details = document.querySelector("#details");
  details.textContent = `${id} — ${parcel.address} — ${parcel.area}`;
  details.hidden = false;
}

// A previous agent checked this URL-loaded fixture and called the click done.
// The rendered parcel buttons still have no click behavior.
const fixture = new URLSearchParams(location.search).get("fixture");
if (fixture) showParcel(fixture);
