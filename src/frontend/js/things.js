let base_url = "/api/v1";


const cnt_gen_things = document.getElementById('cnt_gen_things');
const gen_things_btn = document.getElementById('gen_things_btn');
cnt_gen_things.value = '13';

const things_load_btn = document.getElementById('things_load_btn');
const things_clean_btn = document.getElementById('things_clean_btn');
const things_count = document.getElementById('things_count');
const things_offset = document.getElementById('things_offset');
const things_table_body = document.getElementById('things_table_body');
things_count.value = '5';
things_offset.value = '0';

const thing_id_get_input = document.getElementById('thing_id_get_input');
const thing_id_get_btn = document.getElementById('thing_id_get_btn');
const thing_card = document.getElementById('thing_card');

const thing_delete_all_btn = document.getElementById('thing_delete_all_btn');

const thing_id_delete_input = document.getElementById('thing_id_delete_input');
const thing_id_delete_btn = document.getElementById('thing_id_delete_btn');

for(const num_input_field of [cnt_gen_things, things_offset,
     things_count, thing_id_get_input, thing_id_delete_input]){
    num_input_field.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace('/\D/g',"");
    });
}


function showErr(txt){
    Swal.fire({
            icon: 'error',
            title: 'Input error',
            text: txt,
            });
}

function showToast(txt){
    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: txt,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true
        });
}

function higlightInputErr(inputId, timeMs=2000){
    const inp = document.getElementById(inputId);
    if (!inp) return;
    inp.classList.add('error');
    setTimeout(()=>{inp.classList.remove('error');}, timeMs);
}

gen_things_btn.addEventListener('click', async () => {
    
    try{

        if(cnt_gen_things.value.length==0){
            higlightInputErr('cnt_gen_things');
            showErr('you should specify cnt_gen_things');
            throw new Error(`you should specify cnt_gen_things`);
        }

        let cnt = Number(cnt_gen_things.value);

        const params = new URLSearchParams({
            count: cnt
        });

        if(cnt>67){
            showErr(`cnt is too big: ${cnt}. max is 67`);
            higlightInputErr('cnt_gen_things');
            throw new Error(`cnt is too big: ${cnt}\nmax is 67`);
        }
        
        const res = await fetch(base_url + `/things/generate_things?${params}`, {
            method: 'POST'
        });

        if(!res.ok){
            throw new Error(`failed to generate things l1: ${res.status}`);
        }

        console.log(`generated ${cnt} new things`);
        showToast(`generated ${cnt} new things`)
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});



things_clean_btn.addEventListener('click', () => {
    things_table_body.innerHTML = '';
});

things_load_btn.addEventListener('click', async () => {
    try{
        if(things_count.value.length==0){
            showErr(`you should specify things_count`);
            higlightInputErr('things_count');
            throw new Error(`you should specify things_count`);
        }

        if(things_offset.value.length==0){
            showErr(`you should specify things_offset`);
            higlightInputErr('things_offset');
            throw new Error(`you should specify things_offset`);
        }

        if( Number(things_count.value) > 67 ){
            higlightInputErr('things_count');
            showErr(`${Number(things_count.value)} rows is too many. max is 67`);
            throw new Error(`${Number(things_count.value)} rows is too many\nmax is 67`);
        }

        const params = new URLSearchParams({
            limit: Number(things_count.value),
            offset: Number(things_offset.value)
        })

        const result = await fetch(base_url + `/things?${params}`,{
            method: 'GET'
        })

        if(!result.ok){
            throw new Error("failed to get things");
        }

        const data = await result.json();

        things_table_body.innerHTML='';

        for(const t of data){
            const tr = document.createElement('tr');
            
            tr.innerHTML = `
                <td>${t.thing_id}</td>
                <td>${t.category}</td>
                <td>${t.price}</td>
            `;
            
            things_table_body.appendChild(tr);
        }

    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});


thing_id_get_btn.addEventListener('click', async () => {
    try{
        if(thing_id_get_input.value.length==0){
            showErr(`you must specify thing_id`);
            higlightInputErr('thing_id_get_input');
            throw new Error('you must specify thing_id');
        }

        const tid = Number(thing_id_get_input.value);

        const result = await fetch(base_url + `/things/${tid}`);

        if(!result.ok){
            higlightInputErr('thing_id_get_input');
            showErr(`err:${result.statusText}`);
            throw new Error(`err:${result.statusText}`);
        }
        

        const thing = await result.json();
        thing_card.innerHTML = '';
        thing_card.style.display = 'block';
        for(const [key,val] of Object.entries(thing)){
            const p = document.createElement('p');
            p.textContent = `${key}: ${val}`;
            thing_card.appendChild(p);
        }

    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});



thing_delete_all_btn.addEventListener('click', async () => {
    try{
        const result = await fetch(base_url + '/things', {method: 'DELETE'});
        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});

thing_id_delete_btn.addEventListener('click', async () => {
    try{
        if(thing_id_delete_input.value.length==0){
            showErr(`you must specify thing_id`);
            higlightInputErr('thing_id_delete_input');
            throw new Error('you must specify thing_id');
        }

        const result = await fetch(
            base_url + `/things/${Number(thing_id_delete_input.value)}`,
             {method: 'DELETE'});
        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});