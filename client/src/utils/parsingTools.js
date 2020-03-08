import * as React from 'react';
import { Row} from 'react-bootstrap/';
import { Card, CardBody} from '../components/Card/Card';
import { Link } from 'react-router-dom';


const languages = (object) => {
	const items = [];
	const keys = Object.keys(object);
	keys.forEach((key) => {
		const title = key.split('_').join(' ');
		if (object[key] !== '') {
			items.push(
				<div key={key} style={{ paddingBottom: '5px' }}>
					{title}:{' '}
					{JSON.stringify(object[key]).replace(
						/(^")|("$)/g,
						''
					)}
				</div>
			);
		}
	});
	return (
		<div>
			{items}
		</div>
	);
}

const removeQuotes = (aString) => {
	aString.replace(/(^")|("$)/g, '');
};

const flagSrc = (iso) => {
	const src = `https://www.countryflags.io/${iso}/flat/64.png`;
	return src;
}

const getRate = (originCurrency, destCurrency) => {
  const api = `https://api.exchangeratesapi.io/latest?base=${originCurrency}&symbols=${destCurrency}`;
	fetch(api)
	.then((resp) => console.log('RESP.JSON ', resp.json())) // Transform the data into json
  .then((data) =>{
    console.log('DATAAAAA ', data)
    })
}

const getOtherTrafficSide = (trafficSide) => {
	if(trafficSide === "left"){
		return "right"
	}
	else{
		return "left"
	}
}

const formatingVisa = (visaInfo) => {
	var removed_double_br = visaInfo.replace("<br><br>", '<li>');
	var formatted_visa_info = removed_double_br.replace(/<br>/g, '<li>');
	return formatted_visa_info
}

function addChosenCities(arrayOfCities){
	const items = [];
	arrayOfCities.forEach(citySubscription =>{
		//we should be sending a request id thats why we ghave it a string is too volatile
		const request_id = citySubscription.request_id;
		const cityName = citySubscription.search_term;
		const latitude = citySubscription.latitude;
		const longitude = citySubscription.longitude;
		items.push(
			<Link
				to={`/user_selection?request_id=${request_id}&city=${cityName}&latitude=${latitude}&longitude=${longitude}`}
			>
			<Row
				style={{
					backgroundColor: 'rgb(247,	247,	247)',
					padding: '0.5em',
					borderRadius: '0px'
				}}
				className="justify-content-center"
			>
			<Card
				style={{
					width: '385px',
					height: '255px'
				}}
			>
				<CardBody
					classExtra="chosen-cities">
						{cityName}
				</CardBody>
			</Card>
			</Row>
			</Link>
		);
	});
	return (
		<div>
			{items}
		</div>
	);

}

function addTrendingSpots(arrayOfImages){
	const items = [];
	// console.log(arrayOfImages)
	arrayOfImages.forEach(image =>{
		//const city_in_url = citySubscription.search_term.toLowerCase().replace(' ', ''); // triming the city to match the tag
		const image_url = image.image_link;
		const geolocation = image.geolocation;
		const caption = image.caption;
		items.push(
			<Row
				style={{
					backgroundColor: 'rgb(247,	247,	247)',
					borderRadius: '0px',
					paddingBottom:'500%'
				}}
				className="justify-content-center"
			>
			<Card
				style={{
					width: '385px',
					height: '255px'
				}}
			>
				<CardBody
					style={{
						padding: '0px',
						height: '100%'
				}}
				>
						{/* style={{backgroundImage: `url(${image_url})`}}> */}
						<img
						src={image_url}
						alt="Logo"
						width='100%'
						height='100%'/>
						<div>
							<b>Geo-location: </b>{geolocation}
							<br></br>
							<br></br>
							{caption}
						</div>
				</CardBody>
			</Card>
			</Row>
		);
	});
	return (
		<div>
			{items}
		</div>
	);

}



export { removeQuotes, languages, flagSrc, getRate, getOtherTrafficSide,formatingVisa, addChosenCities,addTrendingSpots };