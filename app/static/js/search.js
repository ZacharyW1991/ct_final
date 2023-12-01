console.log('Starting Search');
pageloader()

function pageloader(){
    console.log('Loading Page');

    const kanjiSearchForm=document.querySelector('#kanji-search-form');
    kanjiSearchForm.addEventListener('submit', e => kanjiSearch(e, 1))
    
    async function kanjiSearch(e){
        e.preventDefault();
        const meaning=document.getElementsByName('meaning')[0].value;
        const nameReading=document.getElementsByName('name-reading')[0].value;
        const onyomi=document.getElementsByName('onyomi')[0].value;
        const kunyomi=document.getElementsByName('kunyomi')[0].value;

        let urlConstruct=[]

        if (meaning){
            urlConstruct.push(`kem=${meaning.toLowerCase()}`)
        }

        if (nameReading){
            urlConstruct.push(`rjn=${nameReading.toLowerCase()}`)
        }

        if (onyomi){
            urlConstruct.push(`on=${onyomi.toLowerCase()}`)
        }

        if (kunyomi){
            urlConstruct.push(`kun=${kunyomi.toLowerCase()}`)
        }

        const url = `https://kanjialive-api.p.rapidapi.com/api/public/search/advanced/?${urlConstruct.join('&')}`;

        const options = {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': '4c9fcfd817msh939e3bd498d9e5ap164e4fjsn8ff062b62217',
                'X-RapidAPI-Host': 'kanjialive-api.p.rapidapi.com'
            }
        };
        
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            console.log(result);
            displayKanji(result)
        } catch (error) {
            console.error(error);
        }
    }

    async function displayKanji(data){
        let table=document.getElementById('kanji-table');

        clearTable(table);

        const thead=document.createElement('thead');
        table.append(thead);
        let tr=document.createElement('tr');
        thead.append(tr);
        const tableHeadings=['Kanji', 'Meaning', 'Strokes', 'Onyomi', 'Kunyomi', 'Name', 'Favorite', 'Remove'];
        tableHeadings.forEach( heading => {
            let th=document.createElement('th');
            th.scope='col';
            th.innerHTML=heading;
            tr.append(th);
        })

        let tbody=document.createElement('tr');
        table.append(tbody);
        for (let k of data){
            const url2=`https://kanjialive-api.p.rapidapi.com/api/public/kanji/${k.kanji.character}`

            const options = {
                method: 'GET',
                headers: {
                    'X-RapidAPI-Key': '4c9fcfd817msh939e3bd498d9e5ap164e4fjsn8ff062b62217',
                    'X-RapidAPI-Host': 'kanjialive-api.p.rapidapi.com'
                }
            };
            let result;
            try {
                const response = await fetch(url2, options);
                result = await response.json();
                console.log(result);
            } catch (error) {
                console.error(error);
            }

            let tr=document.createElement('tr');
            tbody.append(tr);

            newDataCell(tr, result.kanji.character);
            newDataCell(tr, result.kanji.meaning.english);
            newDataCell(tr, result.kanji.strokes.count);
            newDataCell(tr, result.kanji.onyomi.romaji);
            newDataCell(tr, result.kanji.kunyomi.romaji);
            newDataCell(tr, result.kname);
            newDataCell(tr, `<a href='/favorite/${k.kanji.character}'><button>Favorite</button></a>`); 
            newDataCell(tr, `<a href='/delete-kanji/${k.kanji.character}'><button>Delete</button></a>`); 
        }
    }

    function newDataCell(tr, value){
        let td=document.createElement('td');
        td.innerHTML=value ?? '-';
        tr.append(td);
    }

    function clearTable(table){
        table.innerHTML='';
    }
}