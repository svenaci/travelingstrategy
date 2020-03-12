import React, { useState, useEffect } from 'react';
import { Row, Col, Button, Nav } from 'react-bootstrap/';
import Client from 'predicthq';
import { Card, CardBody } from '../components/Card/Card';
import '../App.css';
import { addMyEvents, addApiEvents } from '../utils/eventsTools';


const client = new Client({ access_token: '3ezKmlrAYq3QMDt3d-wZh2q-oBVt57U0c_CfJiax' });
const phqEvents = client.events;


function Events({
	requestId,
	latitude,
	longitude
}) {
	const [category, setCategory] = useState('');
	const [savedEvents, setSavedEvents] = useState([]);
	const [eventsForCategories, setEventsForCategories] = useState([]);
	const [conferences, setConferences] = useState([]);
	const [expos, setExpos] = useState([]);
	const [concerts, seConcerts] = useState([]);
	const [festivals, setFestivals] = useState([]);
	const [performingArts, setPerformingArts] = useState([]);
	const [sports, setSports] = useState([]);
	const [community, setCommunity] = useState([]);
	const [conferencesCalled, setConferencesCalled] = useState(false);
	const [exposCalled, setExposCalled] = useState(false);
	const [concertsCalled, setConcertsCalled] = useState(false);
	const [festivalsCalled, setFestivalsCalled] = useState(false);
	const [performingArtsCalled, setPerformingArtsCalled] = useState(false);
	const [sportsCalled, setSportsCalled] = useState(false);
	const [communityCalled, setCommunityCalled] = useState(false);
	const [toggled,setToggled] = useState(true);
	const [navbarClass, setNavbarClass ] = useState('sidebar sidebar--expanded');
	const [mainContentClass, setMainContentClass ] = useState('main-content main-content--expanded');


	const categoryChosen = (event) => {
		setCategory(event.target.value);
	};

	useEffect(() => {
		// Basic event search using category as parameter. By default, it will return the first ten events.
		async function searchByCategory() {
			console.log('hello')
			const withinParam = `${latitude},${longitude}`;
			const searchResults = await phqEvents.search({
				'location_around.origin': withinParam,
				category
			});
			return searchResults.result.results;
		}
		/**
         * This function checks if the events for a category were already requested
         * in order to provide faster service and limit api calls
         * */
		async function eventsByCategoryToDispaly() {
			let arrayOfEvents = [];
			switch (category) {
				case 'conferences':
					if (!conferencesCalled) {
						arrayOfEvents = await searchByCategory();
						setConferences(arrayOfEvents);
					} else {
						arrayOfEvents = conferences;
					}
					setConferencesCalled(true);
					break;
				case 'expos':
					if (!exposCalled) {
						arrayOfEvents = await searchByCategory();
						setExpos(arrayOfEvents);
					} else {
						arrayOfEvents = expos;
					}
					setExposCalled(true);
					break;
				case 'concerts':
					if (!concertsCalled) {
						arrayOfEvents = await searchByCategory();
						seConcerts(arrayOfEvents);
					} else {
						arrayOfEvents = concerts;
					}
					setConcertsCalled(true);
					break;
				case 'festivals':
					if (!festivalsCalled) {
						arrayOfEvents = await searchByCategory();
						setFestivals(arrayOfEvents);
					} else {
						arrayOfEvents = festivals;
					}
					setFestivalsCalled(true);
					break;
				case 'performing-arts':
					if (!performingArtsCalled) {
						arrayOfEvents = await searchByCategory();
						setPerformingArts(arrayOfEvents);
					} else {
						arrayOfEvents = performingArts;
					}
					setPerformingArtsCalled(true);
					break;
				case 'sports':
					if (!sportsCalled) {
						arrayOfEvents = await searchByCategory();
						setSports(arrayOfEvents);
					} else {
						arrayOfEvents = sports;
					}
					setSportsCalled(true);
					break;
				case 'community':
					if (!communityCalled) {
						arrayOfEvents = await searchByCategory();
						setCommunity(arrayOfEvents);
					} else {
						arrayOfEvents = community;
					}
					setCommunityCalled(true);
					break;
				default:
			}
			return arrayOfEvents;
		}

		async function fetchEvents() {
			await fetch(process.env.REACT_APP_BACKEND, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					query: `{
                        eventsForRequest(request_id:"5"){
                            request_id,
                            event_category,
                              description,
                              duration,
                              start_date,
                              end_date,
                              title,
                              labels,
                              address,
                              place_type,
                              name_of_place
                            }
                    }
                    `
				})
			})
				.then((res) => res.json())
				.then((res) => {
					res.data.eventsForRequest
                    && res.data.eventsForRequest.length !== 0
                    && setSavedEvents(res.data.eventsForRequest);
				});
		}

		async function setEventsToDisplay() {
			const eventsByCategory = await eventsByCategoryToDispaly();
			setEventsForCategories(eventsByCategory);
		}

		fetchEvents();
		setEventsToDisplay();
	},
	[
		category,
		conferences,
		expos,
		concerts,
		festivals,
		performingArts,
		sports,
		community,
		conferencesCalled,
		exposCalled,
		concertsCalled,
		festivalsCalled,
		performingArtsCalled,
		sportsCalled,
		communityCalled,
		latitude,
		longitude

	]);

	

	const expandNavBar= (event) => {
		if(toggled){
			setNavbarClass("sidebar")
			setMainContentClass("main-content")
			setToggled(false)
		}
		else{
			setNavbarClass("sidebar sidebar--expanded")
			setMainContentClass("main-content main-content--expanded")
			setToggled(true)
		}
	}

	return (
		<div>
			<div className={navbarClass}  onClick={expandNavBar}>
				<span className="shape"></span>
				<span className="shape"></span>
				<div className='categories-btn'>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="conferences" onClick={categoryChosen}>Conferences</Button>
					</div>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="expos" onClick={categoryChosen}>Expos</Button>
					</div>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="concerts" onClick={categoryChosen}>Concerts</Button>
					</div>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="festivals" onClick={categoryChosen}>Festivals</Button>
					</div>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="performing-arts" onClick={categoryChosen}>Performing-arts</Button>
					</div>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="sports" onClick={categoryChosen}>Sports</Button>
					</div>
					<div className='choice-btn'>
						<Button variant="outline-primary" style={{width:'100%'}} value="community" onClick={categoryChosen}>Community</Button>
					</div>
				</div>
			</div>
			

			<section className={mainContentClass}>
				<header>
				<span></span>
				<ul>
					<li></li>
					<li></li>
					<li></li>
				</ul>
				</header>
				<div className="container">
				<div className="module--full">
				</div>
				<div className="module-wrapper">
					<div className="module--half">
					</div>
					<div className="module--half">
					</div>
				</div>
				</div>
			</section>
			<div className="parallax">
				<Row className="justify-content-center" style={{ paddingTop: '100px' }}>
					<Col
						style={{
							backgroundColor: 'rgb(255, 255, 255)',
							borderRadius: '20px'
						}}
						lg={8}
					>
						<Row
							style={{
								backgroundColor: 'rgb(247,	247,	247)',
								padding: '0.5em',
								borderRadius: '0px'
							}}
							className="justify-content-center sticky"
						>
							<Nav variant="pills" className="flex-row">
								<Nav.Item>
									<Button variant="outline-primary" value="conferences" onClick={categoryChosen}>Conferences</Button>
								</Nav.Item>
								<Nav.Item>
									<Button variant="outline-primary" value="expos" onClick={categoryChosen}>Expos</Button>
								</Nav.Item>
								<Nav.Item>
									<Button variant="outline-primary" value="concerts" onClick={categoryChosen}>Concerts</Button>
								</Nav.Item>
								<Nav.Item>
									<Button variant="outline-primary" value="festivals" onClick={categoryChosen}>Festivals</Button>
								</Nav.Item>
								<Nav.Item>
									<Button variant="outline-primary" value="performing-arts" onClick={categoryChosen}>Performing-arts</Button>
								</Nav.Item>
								<Nav.Item>
									<Button variant="outline-primary" value="sports" onClick={categoryChosen}>Sports</Button>
								</Nav.Item>
								<Nav.Item>
									<Button variant="outline-primary" value="community" onClick={categoryChosen}>Community</Button>
								</Nav.Item>
							</Nav>
						</Row>
						<div className="justify-content-center">
							<div id="My_Events" style={{ padding: '40px 25px 25px 25px' }}>
								<div>
									<ul>
										{addApiEvents(eventsForCategories, requestId)}
									</ul>
									<ul>
										<Card
											header="Favorite Events"
											style={{ maxHeight: '400px', overflow: 'scroll', padding: '40px 25px 25px 25px', textAlign: 'center' }}
										>
											<CardBody>
												{addMyEvents(savedEvents)}
											</CardBody>
										</Card>
									</ul>
								</div>
							</div>
						</div>
					</Col>
				</Row>
				<footer id="footer" />
			</div>
		</div>
	);
}

export default Events;
