let base_url = "/api/v1";

const cnt_gen_users = document.getElementById('cnt_gen_users');
const gen_users_btn = document.getElementById('gen_users_btn');
cnt_gen_users.value = '13';

const users_load_btn = document.getElementById('users_load_btn');
const users_clean_btn = document.getElementById('users_clean_btn');
const users_count = document.getElementById('users_count');
const users_offset = document.getElementById('users_offset');
const users_table_body = document.getElementById('users_table_body');
users_count.value = '5';
users_offset.value = '0';

const user_id_get_input = document.getElementById('user_id_get_input');
const user_id_get_btn = document.getElementById('user_id_get_btn');
const user_card = document.getElementById('user_card');

const user_delete_all_btn = document.getElementById('user_delete_all_btn');

const user_id_delete_input = document.getElementById('user_id_delete_input');
const user_id_delete_btn = document.getElementById('user_id_delete_btn');

const loc_users_a = document.getElementById('loc_users');
const loc_things_a = document.getElementById('loc_things');
const loc_sales_a = document.getElementById('loc_sales');


// todo: make this more compact
loc_things_a.addEventListener('mousemove', () => {
    loc_users_a.classList.remove('current_page');
    loc_users_a.classList.add('other_page');

    loc_things_a.classList.remove('other_page');
    loc_things_a.classList.add('current_page');
});

loc_things_a.addEventListener('mouseleave', () => {
    loc_things_a.classList.remove('current_page');
    loc_things_a.classList.add('other_page');

    loc_users_a.classList.remove('other_page');
    loc_users_a.classList.add('current_page');
});

loc_sales_a.addEventListener('mousemove', () => {
    loc_users_a.classList.remove('current_page');
    loc_users_a.classList.add('other_page');

    loc_sales_a.classList.remove('other_page');
    loc_sales_a.classList.add('current_page');
});

loc_sales_a.addEventListener('mouseleave', () => {
    loc_sales_a.classList.remove('current_page');
    loc_sales_a.classList.add('other_page');

    loc_users_a.classList.remove('other_page');
    loc_users_a.classList.add('current_page');
});



// so user can only input 0-9 inside numeric fields
for(const num_input_field of [cnt_gen_users, users_offset,
     users_count, user_id_get_input, user_id_delete_input]){
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

function higlightInputErr(inputId, timeMs=3000){
    const inp = document.getElementById(inputId);
    if (!inp) return;
    inp.classList.add('error');
    setTimeout(()=>{inp.classList.remove('error');}, timeMs);
}

async function handleErr(result, pairs=null){
    let msg = 'Unknown server error'
    const err_body = await result.json().catch(() => ({}));

    if(typeof err_body.detail == "string"){
        msg = err_body.detail;
    }
    else if(Array.isArray(err_body.detail)){
        if(pairs != null){
            for(const e of err_body.detail){
                higlightInputErr(pairs[e.loc[1]]);
            }
        }
        msg = err_body.detail.map(
            e => `${e.loc.join('.')}: ${e.msg}` 
        ).join('; ');
    }

    const err = new Error(msg);
    err.status = result.status;
    throw err;
}



gen_users_btn.addEventListener('click', async () => {
    try{
        let cnt = Number(cnt_gen_users.value);

        const params = new URLSearchParams({count: cnt});
        
        const result = await fetch(
            base_url + `/users/generate_users?${params}`, 
            {method: 'POST'}
        );

        if(!result.ok){
            await handleErr(result);
        }

        console.log(`generated ${cnt} new users`);
        showToast(`generated ${cnt} new users`)
    }
    catch(err){
        const txt = `Failed to generate users: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('cnt_gen_users');
    }
});

users_clean_btn.addEventListener('click', () => {
    users_table_body.innerHTML = '';
});

users_load_btn.addEventListener('click', async () => {
    try{
        const params = new URLSearchParams({
            count: Number(users_count.value),
            offset: Number(users_offset.value)
        });

        const result = await fetch(
            base_url + `/users?${params}`,
            {method: 'GET'}
        );

        if(!result.ok){
            await handleErr(
                result,
                {"count"  : "users_count",
                 "offset" : "users_offset"}
            );
        }

        const data = await result.json();

        users_table_body.innerHTML='';

        for(const u of data){
            const tr = document.createElement('tr');
            
            tr.innerHTML = `
                <td>${u.user_id}</td>
                <td>${u.user_name}</td>
                <td>${u.user_age}</td>
                <td class="${u.bought_premium ? 'premium' : 'no-premium'}">${u.bought_premium}</td>
            `;
            
            users_table_body.appendChild(tr);
        }

    }
    catch(err){
        const txt = `Failed to load users: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
    }
});

user_id_get_btn.addEventListener('click', async () => {
    try{

        const uid = Number(user_id_get_input.value);

        const result = await fetch(base_url + `/users/${uid}`);

        if(!result.ok){
            await handleErr(result);
        }
        
        const user = await result.json();
        user_card.innerHTML = '';
        user_card.style.display = 'block';
        for(const [key,val] of Object.entries(user)){
            const p = document.createElement('p');
            p.textContent = `${key}: ${val}`;
            user_card.appendChild(p);
        }

    }
    catch(err){
        const txt = `Failed to get user: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('user_id_get_input');
    }
});

user_delete_all_btn.addEventListener('click', async () => {
    try{
        const result = await fetch(
            base_url + '/users',
            {method: 'DELETE'}
        );
        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});

user_id_delete_btn.addEventListener('click', async () => {
    try{

        const result = await fetch(
            base_url + `/users/${Number(user_id_delete_input.value)}`,
            {method: 'DELETE'}
        );
        
        if(!result.ok){
            await handleErr(result);
        }
        
        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        const txt = `Failed to delete user: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('user_id_delete_input');
    }

});