import {
    handleErr,
    higlightInputErr,
    showErr,
    showToast
} from "./utils.js" 



const base_url = "/api/v1";

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



// todo: make this more compact
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



gen_sales_btn.addEventListener('click', async () => {
    try{
        let cnt = Number(cnt_gen_sales.value);

        const params = new URLSearchParams({count: cnt});

        const result = await fetch(
            base_url + `/sales/generate_sales?${params}`,
            {method: 'POST'}
        );

        if(!result.ok){
            await handleErr(result);
        }

        console.log(`generated ${cnt} new sales`);
        showToast(`generated ${cnt} new sales`)
    }
    catch(err){
        const txt = `Failed to generate sales: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('cnt_gen_sales');
    }
});

sales_clean_btn.addEventListener('click', () => {
    sales_table_body.innerHTML = '';
});

sales_load_btn.addEventListener('click', async () => {
    try{
        const params = new URLSearchParams({
            count: Number(sales_count.value),
            offset: Number(sales_offset.value)
        });

        const result = await fetch(
            base_url + `/sales?${params}`,
            {method: 'GET'}
        );

        if(!result.ok){
            await handleErr(
                result,
                {"count"  : "sales_count",
                 "offset" : "sales_offset"}
            );
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
        const txt = `Failed to load sales: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
    }
});

sale_id_get_btn.addEventListener('click', async () => {
    try{
        const sid = Number(sale_id_get_input.value);

        const result = await fetch(base_url + `/sales/${sid}`);

        if(!result.ok){
            await handleErr(result);
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
        const txt = `Failed to get sale: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('sale_id_get_input');
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
        const result = await fetch(
            base_url + `/sales/${Number(sale_id_delete_input.value)}`,
            {method: 'DELETE'}
        );
        
        if(!result){
            await handleErr(result);
        }

        const data = await result.json();
        showToast(data.log);
    }
    catch(err){
        const txt = `Failed to delete sale: ${err.status}(${err.message})`;
        console.error(txt);
        showErr(txt);
        higlightInputErr('sale_id_delete_input');
    }

});
