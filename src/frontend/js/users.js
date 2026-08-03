let base_url = "http://127.0.0.1:8001/api/v1";


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

for(const num_input_field of [cnt_gen_users, users_offset,
     users_count, user_id_get_input, user_id_delete_input]){
    num_input_field.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace('/\D/g',"");
    });
}



gen_users_btn.addEventListener('click', async () => {
    
    try{

        if(cnt_gen_users.value.length==0){
            alert(`you should specify cnt_gen_users`);
            throw new Error(`you should specify cnt_gen_users`);
        }

        let cnt = Number(cnt_gen_users.value);

        const params = new URLSearchParams({
            count: cnt
        });

        if(cnt>67){
            alert(`cnt is too big: ${cnt}\n max is 67`);
            throw new Error(`cnt is too big: ${cnt}\nmax is 67`);
        }
        
        const res = await fetch(base_url + `/users/generate_users?${params}`, {
            method: 'POST'
        });

        if(!res.ok){
            throw new Error(`failed to generate users l1: ${res.status}`);
        }

        console.log(`generated ${cnt} new users`);
        alert(`generated ${cnt} new users`);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});



users_clean_btn.addEventListener('click', () => {
    users_table_body.innerHTML = '';
});

users_load_btn.addEventListener('click', async () => {
    try{
        if(users_count.value.length==0){
            alert(`you should specify users_count`);
            throw new Error(`you should specify users_count`);
        }

        if(users_offset.value.length==0){
            alert(`you should specify users_offset`);
            throw new Error(`you should specify users_offset`);
        }

        if( Number(users_count.value) > 67 ){
            alert(`${Number(users_count.value)} rows is too many\nmax is 67`);
            throw new Error(`${Number(users_count.value)} rows is too many\nmax is 67`);
        }

        const params = new URLSearchParams({
            limit: Number(users_count.value),
            offset: Number(users_offset.value)
        })

        const result = await fetch(base_url + `/users?${params}`,{
            method: 'GET'
        })

        if(!result.ok){
            throw new Error("failed to get users");
        }

        const data = await result.json();

        users_table_body.innerHTML='';

        for(const u of data){
            const tr = document.createElement('tr');
            
            tr.innerHTML = `
                <td>${u.user_id}</td>
                <td>${u.user_name}</td>
                <td>${u.user_age}</td>
                <td>${u.bought_premium}</td>
            `;

            users_table_body.appendChild(tr);
        }

    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});


user_id_get_btn.addEventListener('click', async () => {
    try{
        if(user_id_get_input.value.length==0){
            alert(`you must specify user_id`);
            throw new Error('you must specify user_id');
        }

        const uid = Number(user_id_get_input.value);

        const result = await fetch(base_url + `/users/${uid}`);

        if(!result.ok){
            alert(`err:${result.statusText}`);
            throw new Error(`err:${result.statusText}`);
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
        console.error(`Some error here l2: ${err}`);
    }
});



user_delete_all_btn.addEventListener('click', async () => {
    try{
        const result = await fetch(base_url + '/users', {method: 'DELETE'});
        const data = await result.json();
        alert(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});

user_id_delete_btn.addEventListener('click', async () => {
    try{
        if(user_id_delete_input.value.length==0){
            alert(`you must specify user_id`);
            throw new Error('you must specify user_id');
        }

        const result = await fetch(
            base_url + `/users/${Number(user_id_delete_input.value)}`,
             {method: 'DELETE'});
        const data = await result.json();
        alert(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});