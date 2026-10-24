function Difficulty({ level }) {
  return <span className={`difficulty ${level.toLowerCase()}`}>{level}</span>
}

export default Difficulty
