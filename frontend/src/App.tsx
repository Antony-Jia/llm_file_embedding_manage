import { useState } from 'react'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<string[]>([])

  const handleSearch = () => {
    setResults([`搜索占位结果：${query}`])
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '1rem' }}>
      <h1>文件向量嵌入平台</h1>
      <p>这是一个根据开发文档搭建的前端占位页面，后续可以接入真实接口。</p>
      <div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="输入搜索内容"
          style={{ padding: '0.5rem', width: '300px' }}
        />
        <button onClick={handleSearch} style={{ marginLeft: '0.5rem', padding: '0.5rem 1rem' }}>
          搜索
        </button>
      </div>
      <ul>
        {results.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </div>
  )
}

export default App
