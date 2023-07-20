template <class T> 
class Array { 
private:   
    T *m_pData;   
    unsigned int m_nSize; 
 
public:  
    Array(unsigned int nSize) : m_nSize(nSize)   {
           if(m_nSize > 0)   
            m_pData = new (nothrow) T[m_nSize];  
    } 
 
    virtual ~Array()  {   
        if(m_pData != NULL)    
        delete m_pData;  
    }
    bool Set(unsigned int nPos, const T& Value)  {
           if(nPos < m_nSize)   {    
            m_pData[nPos] = Value;    return true;   
            }   
            else    return false;  
    } 
 
 T Get(unsigned int nPos)  {
    if(nPos < m_nSize)    
        return m_pData[nPos];   
    else    
        return T();  
    } 
}; 