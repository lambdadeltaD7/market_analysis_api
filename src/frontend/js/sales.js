let base_url = "/api/v1";


const cnt_gen_sales = document.getElementById('cnt_gen_sales');
const gen_sales_btn = document.getElementById('gen_sales_btn');
cnt_gen_sales.value = '13';

const sales_load_btn = document.getElementById('sales_load_btn');
const sales_clean_btn = document.getElementById('sales_clean_btn');
const sales_count = document.getElementById('sales_count');
const sales_offset = document.getElementById('sales_offset');
const sales_table_body = document.getElementById('sales_table_body');
sales_count.value = '5';
sales_offset.value = '0';

const sale_id_get_input = document.getElementById('sale_id_get_input');
const sale_id_get_btn = document.getElementById('sale_id_get_btn');
const sale_card = document.getElementById('sale_card');

const sale_delete_all_btn = document.getElementById('sale_delete_all_btn');

const sale_id_delete_input = document.getElementById('sale_id_delete_input');
const sale_id_delete_btn = document.getElementById('sale_id_delete_btn');


const loc_users_a = document.getElementById('loc_users');
const loc_things_a = document.getElementById('loc_things');
const loc_sales_a = document.getElementById('loc_sales');


loc_users_a.addEventListener('mousemove', () => {
    loc_sales_a.classList.remove('current_page');
    loc_sales_a.classList.add('other_page');

    loc_users_a.classList.remove('other_page');
    loc_users_a.classList.add('current_page');
});

loc_users_a.addEventListener('mouseleave', () => {
    loc_users_a.classList.remove('current_page');
    loc_users_a.classList.add('other_page');

    loc_sales_a.classList.remove('other_page');
    loc_sales_a.classList.add('current_page');
});


loc_things_a.addEventListener('mousemove', () => {
    loc_sales_a.classList.remove('current_page');
    loc_sales_a.classList.add('other_page');

    loc_things_a.classList.remove('other_page');
    loc_things_a.classList.add('current_page');
});

loc_things_a.addEventListener('mouseleave', () => {
    loc_things_a.classList.remove('current_page');
    loc_things_a.classList.add('other_page');

    loc_sales_a.classList.remove('other_page');
    loc_sales_a.classList.add('current_page');
});




for(const num_input_field of [cnt_gen_sales, sales_offset,
     sales_count, sale_id_get_input, sale_id_delete_input]){
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

gen_sales_btn.addEventListener('click', async () => {
    
    try{

        if(cnt_gen_sales.value.length==0){
            higlightInputErr('cnt_gen_sales');
            showErr('you should specify cnt_gen_sales');
            throw new Error(`you should specify cnt_gen_sales`);
        }

        let cnt = Number(cnt_gen_sales.value);

        const params = new URLSearchParams({
            count: cnt
        });

        if(cnt>67){
            showErr(`cnt is too big: ${cnt}. max is 67`);
            higlightInputErr('cnt_gen_sales');
            throw new Error(`cnt is too big: ${cnt}\nmax is 67`);
        }
        
        const res = await fetch(base_url + `/sales/generate_sales?${params}`, {
            method: 'POST'
        });

        if(!res.ok){
            throw new Error(`failed to generate sales l1: ${res.status}`);
        }

        console.log(`generated ${cnt} new sales`);
        showToast(`generated ${cnt} new sales`)
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});



sales_clean_btn.addEventListener('click', () => {
    sales_table_body.innerHTML = '';
});

sales_load_btn.addEventListener('click', async () => {
    try{
        if(sales_count.value.length==0){
            showErr(`you should specify sales_count`);
            higlightInputErr('sales_count');
            throw new Error(`you should specify sales_count`);
        }

        if(sales_offset.value.length==0){
            showErr(`you should specify sales_offset`);
            higlightInputErr('sales_offset');
            throw new Error(`you should specify sales_offset`);
        }

        if( Number(sales_count.value) > 67 ){
            higlightInputErr('sales_count');
            showErr(`${Number(sales_count.value)} rows is too many. max is 67`);
            throw new Error(`${Number(sales_count.value)} rows is too many\nmax is 67`);
        }

        const params = new URLSearchParams({
            limit: Number(sales_count.value),
            offset: Number(sales_offset.value)
        })

        const result = await fetch(base_url + `/sales?${params}`,{
            method: 'GET'
        })

        if(!result.ok){
            throw new Error("failed to get sales");
        }

        const data = await result.json();

        sales_table_body.innerHTML='';

        for(const s of data){
            const tr = document.createElement('tr');
            
            tr.innerHTML = `
                <td>${s.sale_id}</td>
                <td>${s.user_id}</td>
                <td>${s.thing_id}</td>
                <td>${s.count}</td>
                <td>${s.payment_type}</td>
                <td>${s.sale_time}</td>
            `;
            
            sales_table_body.appendChild(tr);
        }

    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});


sale_id_get_btn.addEventListener('click', async () => {
    try{
        if(sale_id_get_input.value.length==0){
            showErr(`you must specify sale_id`);
            higlightInputErr('sale_id_get_input');
            throw new Error('you must specify sale_id');
        }

        const sid = Number(sale_id_get_input.value);

        const result = await fetch(base_url + `/sales/${sid}`);

        if(!result.ok){
            higlightInputErr('sale_id_get_input');
            showErr(`err:${result.statusText}`);
            throw new Error(`err:${result.statusText}`);
        }
        

        const sale = await result.json();
        sale_card.innerHTML = '';
        sale_card.style.display = 'block';
        for(const [key,val] of Object.entries(sale)){
            const p = document.createElement('p');
            p.textContent = `${key}: ${val}`;
            sale_card.appendChild(p);
        }

    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }
});



sale_delete_all_btn.addEventListener('click', async () => {
    try{
        const result = await fetch(base_url + '/sales', {method: 'DELETE'});
        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});

sale_id_delete_btn.addEventListener('click', async () => {
    try{
        if(sale_id_delete_input.value.length==0){
            showErr(`you must specify sale_id`);
            higlightInputErr('sale_id_delete_input');
            throw new Error('you must specify sale_id');
        }

        const result = await fetch(
            base_url + `/sales/${Number(sale_id_delete_input.value)}`,
             {method: 'DELETE'});
        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        console.error(`Some error here l2: ${err}`);
    }

});
