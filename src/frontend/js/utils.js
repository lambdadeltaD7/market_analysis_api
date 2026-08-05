
export function showErr(txt){
    Swal.fire({
            icon: 'error',
            title: 'Input error',
            text: txt,
            });
}

export function showToast(txt){
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

export function higlightInputErr(inputId, timeMs=3000){
    const inp = document.getElementById(inputId);
    if (!inp) return;
    inp.classList.add('error');
    setTimeout(()=>{inp.classList.remove('error');}, timeMs);
}

export async function handleErr(result, pairs=null){
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