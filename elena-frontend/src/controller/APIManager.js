
const postGetPath = async (data) => {
    let resp = await fetch('http://localhost:5000//get-path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': String.valueOf(data.length),
            'Host': 'localhost:5000'
        },
        body: data
    }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            return data
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    return resp
}

export default postGetPath

