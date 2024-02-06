import { useState, useEffect, useRef } from 'react'
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './App.css'

const FETCH_URL = 'http://localhost:8000';

type EmbarkLocation = 'C' | 'Q' | 'S';
type Sex = 'male' | 'female';

interface Passenger {
  passenger_id: number;
  p_class: number;
  name: string;
  sex: Sex;
  age: number;
  nb_sibling_spouse: number;
  nb_parent_children: number;
  ticket: string;
  fare: number;
  cabin: string;
  embark_location: EmbarkLocation;
}

interface ChartType {
  p_class: number;
  male: number;
  female: number;
}

const App = () => {
  const [passengers, setPassengersData] = useState<Passenger[]>([]);
  const [chartsData, setChartsData] = useState<ChartType[]>([]);
  const [searchValue, setSearchValue] = useState<string | undefined>('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchData = async() => {
      const data = await fetch(`${FETCH_URL}/passengers/?search_value=${searchValue}`);
      const passengerData = await data.json();
      setPassengersData(passengerData);
      setChartsData(passengerData.reduce((acc: ChartType[], passenger: Passenger) => {
        if (passenger.sex === 'male') {
          acc[passenger.p_class - 1].male += 1;
        } else if (passenger.sex === 'female') {
          acc[passenger.p_class - 1].female += 1;
        }
        return acc;
      }, [
        { p_class: 1, male: 0, female: 0 },
        { p_class: 2, male: 0, female: 0 },
        { p_class: 3, male: 0, female: 0 }
      ]));
    };

    fetchData();
  }, [searchValue]);

  return (
    <>
      <h1>Titanic Viewer 🧊🚢</h1>
      <div className='search-container'>
        <input type='text' ref={inputRef} placeholder='Filter by passenger name' />
        <button onClick={() => setSearchValue(inputRef?.current?.value)}>Search</button>
      </div>
      <h2>Chart</h2>
      <h3>Repartion of male and female passengers by ticket class</h3>
      <div style={{ height: '500px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              width={500}
              height={500}
              data={chartsData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="p_class" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="male" fill="#8884d8" activeBar={<Rectangle fill="pink" stroke="blue" />} />
              <Bar dataKey="female" fill="#82ca9d" activeBar={<Rectangle fill="blue" stroke="purple" />} />
            </BarChart>
          </ResponsiveContainer>
      </div>
      <h2>All values</h2>
      <table>
        <thead>
          <tr>
            <th>Passenger ID</th>
            <th>Class</th>
            <th>Name</th>
            <th>Sex</th>
            <th>Age</th>
            <th>Nb Sibling Spouse</th>
            <th>Nb Parent Children</th>
            <th>Ticket</th>
            <th>Fare</th>
            <th>Cabin</th>
            <th>Embark Location</th>
          </tr>
        </thead>
        <tbody>
          {passengers.map((passenger: Passenger) => (
            <tr key={passenger.passenger_id}>
              <td>{passenger?.passenger_id}</td>
              <td>{passenger?.p_class}</td>
              <td>{passenger?.name}</td>
              <td>{passenger?.sex}</td>
              <td>{passenger?.age}</td>
              <td>{passenger?.nb_sibling_spouse}</td>
              <td>{passenger?.nb_parent_children}</td>
              <td>{passenger?.ticket}</td>
              <td>{passenger?.fare}</td>
              <td>{passenger?.cabin}</td>
              <td>{passenger?.embark_location}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export default App
