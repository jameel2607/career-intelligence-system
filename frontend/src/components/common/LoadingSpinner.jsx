export default function LoadingSpinner(){
  return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'center',padding:'24px'}}>
      <div style={{width:24,height:24,border:'3px solid #e5e7eb',borderTopColor:'#2563eb',borderRadius:'50%',animation:'spin 1s linear infinite'}} />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  )
}
