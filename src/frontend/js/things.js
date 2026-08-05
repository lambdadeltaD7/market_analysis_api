import {
    handleErr,
    higlightInputErr,
    showErr,
    showToast
} from "./utils.js" 



let base_url = "/api/v1";

const cnt_gen_things = document.getElementById('cnt_gen_things');
const gen_things_btn = document.getElementById('gen_things_btn');
cnt_gen_things.value = '13';

const things_load_btn = document.getElementById('things_load_btn');
const things_clean_btn = document.getElementById('things_clean_btn');
const things_count = document.getElementById('things_count');
const things_offset = document.getElementById('things_offset');
const things_table_body = document.getElementById('things_table_body');


const thing_id_get_input = document.getElementById('thing_id_get_input');
const thing_id_get_btn = document.getElementById('thing_id_get_btn');
const thing_card = document.getElementById('thing_card');

const thing_delete_all_btn = document.getElementById('thing_delete_all_btn');

const thing_id_delete_input = document.getElementById('thing_id_delete_input');
const thing_id_delete_btn = document.getElementById('thing_id_delete_btn');

const loc_users_a = document.getElementById('loc_users');
const loc_things_a = document.getElementById('loc_things');
const loc_sales_a = document.getElementById('loc_sales');



// todo: make this more compact
loc_users_a.addEventListener('mousemove', () => {
    loc_things_a.classList.remove('current_page');
    loc_things_a.classList.add('other_page');

    loc_users_a.classList.remove('other_page');
    loc_users_a.classList.add('current_page');
});

loc_users_a.addEventListener('mouseleave', () => {
    loc_users_a.classList.remove('current_page');
    loc_users_a.classList.add('other_page');

    loc_things_a.classList.remove('other_page');
    loc_things_a.classList.add('current_page');
});

loc_sales_a.addEventListener('mousemove', () => {
    loc_things_a.classList.remove('current_page');
    loc_things_a.classList.add('other_page');

    loc_sales_a.classList.remove('other_page');
    loc_sales_a.classList.add('current_page');
});

loc_sales_a.addEventListener('mouseleave', () => {
    loc_sales_a.classList.remove('current_page');
    loc_sales_a.classList.add('other_page');

    loc_things_a.classList.remove('other_page');
    loc_things_a.classList.add('current_page');
});



// so user can only input 0-9 inside numeric fields
for(const num_input_field of [cnt_gen_things, things_offset,
     things_count, thing_id_get_input, thing_id_delete_input]){
    num_input_field.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace('/\D/g',"");
    });
}



gen_things_btn.addEventListener('click', async () => {
    try{
        let cnt = Number(cnt_gen_things.value);

        const params = new URLSearchParams({count: cnt});
        
        const result = await fetch(
            base_url + `/things/generate_things?${params}`, 
            {method: 'POST'}
        );

        if(!result.ok){
            await handleErr(result);
        }

        console.log(`generated ${cnt} new things`);
        showToast(`generated ${cnt} new things`);
    }
    catch(err){
        const txt = `Failed to generate things: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('cnt_gen_things');
    }
});

things_clean_btn.addEventListener('click', () => {
    things_table_body.innerHTML = '';
});

things_load_btn.addEventListener('click', async () => {
    try{
        const params = new URLSearchParams({
            count: Number(things_count.value),
            offset: Number(things_offset.value)
        });

        const result = await fetch(
            base_url + `/things?${params}`,
            {method: 'GET'}
        );

        if(!result.ok){
            await handleErr(
                result,
                {"count"  : "things_count",
                 "offset" : "things_offset"}
            );
        };

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
        const txt = `Failed to load things: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
    }
});

thing_id_get_btn.addEventListener('click', async () => {
    try{
        const tid = Number(thing_id_get_input.value);

        const result = await fetch(base_url + `/things/${tid}`);

        if(!result.ok){
            await handleErr(result);
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
        const txt = `Failed to get thing: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('thing_id_get_input');
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
        const result = await fetch(
            base_url + `/things/${Number(thing_id_delete_input.value)}`,
            {method: 'DELETE'}
        );

        if(!result.ok){
            await handleErr(result);
        }

        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        const txt = `Failed to delete thing: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('thing_id_delete_input');
    }

});