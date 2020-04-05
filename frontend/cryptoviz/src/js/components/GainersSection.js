import "bootswatch/dist/lux/bootstrap.min.css";
import React, { useEffect, useState, useContext } from "react";
import { useInterval } from '../api/common';
import { trackPromise } from 'react-promise-tracker';
import { Spinner } from './Spinner';
import { areas } from '../constants/areas';
import { AuthContext } from "./App";
import "../../style/main.css";
import Cookies from 'js-cookie';

function GainersSection() {
  const { state: authState, dispatch } = useContext(AuthContext);
  const [gainersTimeInterval, setGainersTimeInterval] = useState("1");
  const [errorMessage, setErrorMessage] = useState("");
  const [gainers, setGainers] = useState([]);

  useInterval(() => {
    getGainers();
  }, 30000);

  useEffect(() => {
    setGainers([]);
    trackPromise(getGainers(), areas.gainers);
  }, [gainersTimeInterval]);

  const getGainers = async () => {
    try {
      let response = await fetch(`http://localhost:8000/api/gainers/?time=${gainersTimeInterval}`);
      let data = await response.json();
      if (!response.ok) {
        const error = (data && data.detail) ? data.detail : response.status;
        console.error("There was an error!", error);
        return;
      }
      setGainers(data.gainers);
    } catch(error) {
      console.error("There was an error!", error);
    }
  };

  const updateUser = async (updatedUser) => {
    const requestOptions = {
      method: 'PATCH',
      headers: {
        'Authorization': 'Bearer ' + Cookies.get('user_auth')
      },
      body: JSON.stringify(updatedUser),
      credentials: 'include'
    };
    try {
      let response = await fetch('http://localhost:8000/api/users/me', requestOptions);
      let data = await response.json();
      if (!response.ok) {
        const error = (data && data.detail) ? data.detail : response.status;
        setErrorMessage(error);
        console.error("There was an error!", error);
        return;
      }
      setErrorMessage('');
      dispatch({
        type: "LOGIN",
        payload: {
          user: updatedUser
        }
      });
    } catch(error) {
      setErrorMessage(error);
      console.error("There was an error!", error);
    }
  }

  const deleteFromWatchlist = ele => {
    let eleIndex = authState.user.watchlist.indexOf(ele);
    let tmp = JSON.parse(JSON.stringify(authState.user));
    tmp.watchlist.splice(eleIndex, 1);
    updateUser(tmp);
  }

  const addToWatchlist = ele => {
    console.log(authState.user);
    let tmp = JSON.parse(JSON.stringify(authState.user));
    tmp.watchlist.push(ele);
    updateUser(tmp);
  }

  const timeMapping = {
    "1": "1 Hour",
    "24": "1 Day"
  };

  const createTable = data => {
    let rows = [];
    let rowClass = "table-primary";
    let cells = [];
    let count = 0;
    for (let i = 0; i < data.length; i++) {
      cells.push(
        <td key={count}>{data[i].rank}</td>
      );
      cells.push(
        <td key={count + 1}>{data[i].symbol}</td>
      );
      cells.push(
        <td key={count + 2}>{data[i].market_cap}</td>
      );
      cells.push(
        <td key={count + 3}>{data[i].price}</td>
      );
      cells.push(
        <td key={count + 4}>{data[i].volume}</td>
      );
      count += 5;
      if (Object.keys(authState.user).length > 0) {
        if (authState.user.watchlist.includes(data[i].symbol)) {
          cells.push(
            <td key={count}><div className="delete-icon" data-toggle="tooltip" data-placement="top" title="" data-original-title="Remove from watchlist" onClick={() => deleteFromWatchlist(data[i].symbol)}/></td>
          );
        } else {
          cells.push(
            <td key={count}><div className="add-icon" data-toggle="tooltip" data-placement="top" title="" data-original-title="Add to watchlist" onClick={() => addToWatchlist(data[i].symbol)}/></td>
          );
        }
        count += 1;
      }
      rows.push(
        <tr key={count} className={rowClass}>
          {cells}
        </tr>
      );
      rowClass = rowClass === "table-primary" ? "table-secondary" : "table-primary";
      count += 1;
      cells = [];
    }
    return rows;
  };

  return (
      <div style={{ textAlign: "center"}}>
        {errorMessage && <div style={{margin: "auto", textAlign: "center"}} className="toast show" role="alert" aria-live="assertive" aria-atomic="true">
          <div className="toast-header">
            <div className="mr-auto">Error</div>
              <button type="button" className="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close" onClick={() => {setErrorMessage('')}}>
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="toast-body">
            {errorMessage}
          </div>
        </div>}
        <h1 style={{ marginTop: "2em" }}>Top 10 Gainers ({timeMapping[gainersTimeInterval]})</h1>
        <div style={{ marginTop: "2em" }}>
          <div
            className="btn-group"
            role="group"
            aria-label="Button group with nested dropdown"
          >
            <button type="button" className="btn btn-primary">
              Select Time Interval
            </button>
            <div className="btn-group" role="group">
              <button
                id="btnGroupDrop1"
                type="button"
                className="btn btn-primary dropdown-toggle"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              ></button>
              <div className="dropdown-menu" aria-labelledby="btnGroupDrop1">
                <a
                  href="#"
                  className="dropdown-item"
                  onClick={() => {
                    setGainersTimeInterval("1");
                  }}
                >
                  {timeMapping["1"]}
                </a>
                <a
                  href="#"
                  className="dropdown-item"
                  onClick={() => {
                    setGainersTimeInterval("24");
                  }}
                >
                  {timeMapping["24"]}
                </a>
              </div>
            </div>
          </div>
        </div>
        <div style={{marginTop: "4em"}}>
          <table className="table table-hover">
            <thead>
              <tr>
                <th scope="col">Rank</th>
                <th scope="col">Symbol</th>
                <th scope="col">Market Cap</th>
                <th scope="col">Price</th>
                <th scope="col">Volume</th>
                {Object.keys(authState.user).length > 0 && <th scope="col">Action</th>}
              </tr>
            </thead>
            <tbody>{createTable(gainers)}</tbody>
          </table>
          <Spinner area={areas.gainers}/>
        </div>
      </div>
  );
}

export default GainersSection;
