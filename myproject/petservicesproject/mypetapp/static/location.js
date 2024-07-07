url1="https://api.postalpincode.in/pincode/"


btn=document.querySelector(".sub")
form=document.getElementById('form')
form.addEventListener("submit",(event)=>{
    event.preventDefault()
    const formdata=new FormData(form)
    console.log(formdata.get('pin'))
    inp=formdata.get('pin')
    pincode(inp)
})

btn.addEventListener("click",()=>{
    formloc=document.querySelector(".formloc")
    formloc.classList.add("formloc1")
})

    async function pincode(inp){    
    // inp=document.querySelector('input').value
    getpincode=await getpin(inp)
   
    // selectBlock=document.querySelector("#Block")
    selectName=document.querySelector("#Name")
    selectCircle=document.querySelector("#Circle")
    selectDistrict=document.querySelector("#District")
    selectDivision=document.querySelector("#Division")
    // selectBlock.innerHTML =`<option value="">select Block</option>`; // Clear any existing options
    selectName.innerHTML =`<option value="">select Name</option>`; // Clear any existing options
    selectCircle.innerHTML =`<option value="">select Circle</option>`; // Clear any existing options
    selectDistrict.innerHTML =`<option value="">select District</option>`; // Clear any existing options
    selectDivision.innerHTML =`<option value="">select Division</option>`; // Clear any existing options
    if (getpincode) {
        getpincode.forEach(pincode => {
            // const blockoption = document.createElement('option');
            // blockoption.value = pincode.Block; // You can set value to any unique identifier
            // blockoption.innerHTML =pincode.Block;
            // selectBlock.appendChild(blockoption);
   
      
            const nameoption=document.createElement('option');
            nameoption.value=pincode.Name;
            nameoption.innerHTML=pincode.Name;
            selectName.appendChild(nameoption);

            const circleoption=document.createElement('option');
            circleoption.value=pincode.Circle;
            circleoption.innerHTML=pincode.Circle;
            selectCircle.appendChild(circleoption);
 
     
            const districtoption=document.createElement('option');
            districtoption.value=pincode.District;
            districtoption.innerHTML=pincode.District;
            selectDistrict.appendChild(districtoption);
  
            const divisionoption=document.createElement('option');
            divisionoption.value=pincode.Division;
            divisionoption.innerHTML=pincode.Division;
            selectDivision.appendChild(divisionoption);
        })
    }
}
    
    // {Block: 'Uran', Name: 'Jasai', Circle: 'Maharashtra', District: 'Raigarh(MH)', Division: 'New Mumbai'}
    
    


    async function getpin(inp) {
        try {
            const response = await fetch(url1 + inp);
            const data = await response.json();
            if (data[0].Status === "Success" && data[0].PostOffice) {
                const postOffices = data[0].PostOffice;
                const details = postOffices.map(postOffice => ({
                    // Block: postOffice.Block,
                    Name: postOffice.Name,
                    Circle: postOffice.Circle,
                    District: postOffice.District,
                    Division: postOffice.Division
                }));
                return details;
            } else {
                console.error('No PostOffice data available');
                return [];
            }
        } catch (error) {
            console.error('Fetch error:', error);
            return [];
        }
    }